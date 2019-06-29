import hashlib
import os
import typing

from urllib.parse import urljoin

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from analytics.models import Engagements


class MailingListManager(models.Manager):

    def for_user(self, user):
        return super(MailingListManager, self).get_queryset().filter(user=user)


class BroadCastManager(models.Manager):

    def for_user(self, user):
        mailinglists = MailingList.objects.filter(user=user)
        return super(BroadCastManager, self).get_queryset().filter(mailinglist_id__in=mailinglists)


class SegmentManager(models.Manager):

    def for_user(self, user):
        return super(SegmentManager, self).get_queryset().filter(user=user)


class BulkInsertManager(models.Manager):
    """
    based on https://gist.github.com/datamafia/9671827
    """
    def bulk_insert_ignore(self, create_fields, values, print_sql=False):
        '''
        Bulk insert/ignore
        @param create_fields : list, required, fields for the insert field declaration
        @param values : list of tuples. each tuple must have same len() as create_fields
        @param print_sql : bool, opotional, print to screen for debugging. True required to
            to print exception
        Notes on usage :
            create_fields = ['f1', 'f2', 'f3']
            values = [
                (1, 2, 3),
                (4, 5, 6),
                (5, 3, 8)
            ]
        Example usage :
            modelName.objects._bulk_insert_ignore(
                create_fields,
                values
            )
        Remember to add to model declarations:
            objects = BulkInsertManager() # custom manager
        @return False on fail
        '''
        from django.db import connection, transaction
        cursor = connection.cursor()

        db_table = self.model._meta.db_table

        values_sql = []
        values_sql.append( "(%s)" % (','.join([ " %s " for i in range(len(create_fields))]),))  # correct format

        base_sql = "INSERT IGNORE INTO %s (%s) VALUES " % (db_table, ",".join(create_fields))
        sql = """%s %s""" % (base_sql, ", ".join(values_sql))
        try:
            with transaction.atomic():
                cursor.executemany(sql, values)
            if print_sql is True:
                try:
                    print(cursor._last_executed)
                except Exception as err:
                    pass
            return True
        except Exception as e:
            try :
                print (cursor._last_executed)
            except :
                pass
            if print_sql is True:
                print (e)
            return False

    def bulk_insert_on_duplicate(self, create_fields, values, update_fields, print_sql=False):
        '''
        Bulk insert, update on duplicate key
        @param create_fields : list, required, fields for the insert field declaration
        @param values : list of tuples. each tuple must have same len() as create_fields
        @param update_fields : list, field names to update when duplicate key is detected
        @param print_sql : bool, opotional, print to screen. True required to to print exception
        @return False on fail
        Notes on usage :
            create_fields = ['f1', 'f2', 'f3']
            values = [
                (1, 2, 3),
                (4, 5, 6),
                (5, 3, 8)
            ]
        Example usage :
            modelName.objects._bulk_insert_ignore(
                create_fields,
                values
            )
        Usage notes for update_fields :
            update_fields = ['f1', 'f2']
            where f1, f2 are not part of the unique declaration and represent
                fields to be updated on duplicate key
        Remember to add to model declarations:
            objects = BulkInsertManager() # custom manager
        '''
        from django.db import connection, transaction
        cursor = connection.cursor()

        db_table = self.model._meta.db_table

        values_sql = []
        values_sql.append( "(%s)" % (','.join([ " %s " for i in range(len(create_fields))]),) )

        base_sql = "INSERT INTO %s (%s) VALUES " % (db_table, ",".join(create_fields))

        duplicate_syntax = 'ON DUPLICATE KEY UPDATE '  # left side
        comma = len(update_fields) # verbose placement of comma
        for f in update_fields :
            comma = comma-1
            duplicate_syntax = duplicate_syntax+" "+f+'= values(%s)'% (f)
            if comma > 0 : # place a comma
                duplicate_syntax = duplicate_syntax+','

        sql = """%s %s %s""" % (base_sql, ", ".join(values_sql), duplicate_syntax)

        try:
            with transaction.atomic():
                cursor.executemany(sql, values)
            if print_sql is True:
                try :
                    print (cursor._last_executed)
                except :
                    pass
            return True
        except Exception as e:
            try :
                print (cursor._last_executed)
            except :
                pass
            if print_sql is True :
                print (e)
            return False


class RecipientManager(BulkInsertManager):

    def get_recipients_for_sending(self, mailinglist_ids: typing.List[int] = None) -> models.QuerySet:
        """Provides active & subscribed recipients
        optionally filters by mailinglist_ids if given

        :param mailinglist_ids: list of integers, default None
        :return: QuerySet object
        """
        filter_args = models.Q(unsubscribed=False) & models.Q(inactive=False)
        if mailinglist_ids:
            filter_args &= models.Q(mailinglist_id__in=mailinglist_ids)

        return self.filter(filter_args)

    def get_engaged_recipients(self, mailing_list_id: int) -> models.QuerySet:
        """
        Get engaged recipients from the given Mailing List. Engaged recipient
        has either non-zero number of clicks or non-zero number of opens.

        :param mailing_list_id: id of given mailing list
        :return: QuerySet object
        """
        return self.get_recipients_for_sending([mailing_list_id]).filter(
            models.Q(total_opens__gt=0) | models.Q(total_clicks__gt=0)
        ) | self.get_recipients_for_sending([mailing_list_id]).filter(
            email__in=Engagements.objects.filter(
                listid=str(mailing_list_id)
            ).filter(
                models.Q(event_type='engine_open') | models.Q(event_type='engine_click')
            ).values_list('email', flat=True)
        )


class MailingList(models.Model):

    PROCESSING_TASK_PATH = 'scheduler.tasks.process_mailinglist'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_opens = models.IntegerField(default=0)
    total_clicks = models.IntegerField(default=0)
    total_complaints = models.IntegerField(default=0)
    total_bounces = models.IntegerField(default=0)
    total_sends = models.IntegerField(default=0)
    total_unsubscribes = models.IntegerField(default=0)
    total_recipients = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = MailingListManager()

    def __str__(self):
        return self.name

    def total_delivered(self):
        return self.total_sends - self.total_bounces

    def update_fields(self, **kwargs):
        self.__class__.objects.filter(pk=self.pk).update(**kwargs)

    def write_csv_in_response(self, writer):
        """
        :param writer: CSV writer with connected Django response object

        Updates the Django response object with the mailing list
        serialized to CSV. Serialization of related Recipients is
        implemented in `Recipient.to_csv_row` method.
        """
        writer.writerow([
            'email',
            'first_name',
            'last_name',
            'address1',
            'address2',
            'city',
            'state',
            'zip',
            'country',
            'fax',
            'phone',
            'custom1',
            'custom2',
            'custom3',
            'custom4',
            'custom5',
            'custom6',
            'custom7',
            'custom8',
            'custom9',
            'custom10',
            'total_opens',
            'total_clicks',
            'unsubscribed'
        ])
        for recipient in self.recipient_set.all():
            writer.writerow(recipient.to_csv_row())


class Recipient(models.Model):

    mailinglist = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    email = models.EmailField()
    email_hash = models.CharField(max_length=32, db_index=True)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    address1 = models.CharField(max_length=255, default='')
    address2 = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    zip = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    fax = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=255, default='')
    custom1 = models.CharField(max_length=255, default='')
    custom2 = models.CharField(max_length=255, default='')
    custom3 = models.CharField(max_length=255, default='')
    custom4 = models.CharField(max_length=255, default='')
    custom5 = models.CharField(max_length=255, default='')
    custom6 = models.CharField(max_length=255, default='')
    custom7 = models.CharField(max_length=255, default='')
    custom8 = models.CharField(max_length=255, default='')
    custom9 = models.CharField(max_length=255, default='')
    custom10 = models.CharField(max_length=255, default='')
    unsubscribed = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    total_opens = models.IntegerField(default=0)
    total_clicks = models.IntegerField(default=0)
    total_complaints = models.IntegerField(default=0)
    total_bounces = models.IntegerField(default=0)
    total_sends = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RecipientManager()

    @staticmethod
    def hash_email(email: str) -> str:
        """
        Hashes the given email address

        :param email: email to be hashed
        :return: hash of given email
        """
        return hashlib.md5(email.encode('utf-8')).hexdigest()

    def get_unsubscribe_key(self) -> str:
        return '{}:{}'.format(self.pk, self.email_hash)

    # TODO(dmitry): cover with tests
    def get_unsubscribe_url(self, absolute_root_uri: str = None) -> str:
        # we can't rely on settings, bc celery workers will access another state of memory
        return urljoin(
            absolute_root_uri or settings.ABSOLUTE_ROOT_URI,
            reverse('mailinglist-unsubscribe', args=[self.get_unsubscribe_key()]))

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.email_hash = self.hash_email(self.email)
        super(Recipient, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    def to_csv_row(self) -> typing.List:
        """
        Serialize the data of the instance to be used in CSV export.
        CSV writer expects each row to be the list. That's why we
        generate the list here.
        """
        return [
            self.email,
            self.first_name,
            self.last_name,
            self.address1,
            self.address2,
            self.city,
            self.state,
            self.zip,
            self.country,
            self.fax,
            self.phone,
            self.custom1,
            self.custom2,
            self.custom3,
            self.custom4,
            self.custom5,
            self.custom6,
            self.custom7,
            self.custom8,
            self.custom9,
            self.custom10,
            self.total_opens,
            self.total_clicks,
            'yes' if self.unsubscribed else 'no'
        ]

    class Meta:
        unique_together = (("mailinglist", "email"),)


class Suppression(models.Model):

    email_hash = models.CharField(max_length=32, db_index=True, unique=True)

    objects = BulkInsertManager()


class Broadcast(models.Model):

    mailinglist = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default=None)
    specified_mailinglists = models.TextField(null=True)
    specified_segments = models.TextField(null=True)
    ignored_subscribers = models.TextField(null=True)
    from_name = models.CharField(max_length=255, null=True)
    from_email = models.EmailField(null=True)
    send_time = models.BooleanField(default=False)
    paused_time = models.BooleanField(default=False)
    specified_time = models.DateTimeField(auto_now_add=False, null=True)
    add_unsubscribe_text = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachment/')
    periodic_task = models.ForeignKey(PeriodicTask, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    total_opens = models.IntegerField(default=0)
    total_clicks = models.IntegerField(default=0)
    total_complaints = models.IntegerField(default=0)
    total_bounces = models.IntegerField(default=0)
    total_sends = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sending_details = models.ForeignKey('injector.SendingDetails', null=True, on_delete=models.SET_NULL)

    objects = BroadCastManager()

    def total_delivered(self):
        return self.total_sends - self.total_bounces

    def filename(self):
        return os.path.basename(self.attachment.name)

    def save(self, *args, **kwargs):
        from account.models import Profile
        # fallback to default sending details in Profile
        if not self.sending_details:
            profile = Profile.objects.get(user=self.mailinglist.user)
            self.sending_details = profile.sending_details
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Variant(models.Model):

    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, default=None)
    html_message = models.TextField(null=True)
    remarket_pixel = models.TextField(null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Variant, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject


class Segment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    operation = models.IntegerField(default=0)
    content = models.TextField(null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = SegmentManager()

    def save(self, *args, **kwargs):
        super(Segment, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventDbQuery(models.Model):

    LOOKUP_EVENT_BOUNCE = 'bounce_bad_address'
    LOOKUP_EVENT_SPAM = 'scomp'

    event_type = models.CharField(
        max_length=200
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return "{}-{}".format(self.event_type, self.created)
