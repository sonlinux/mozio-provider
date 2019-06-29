var form = $(".broadcast-wizard").show();

$.validator.addMethod("minDate", function(value, element) {
    var curDate = new Date();
    var inputDate = new Date(value);
    if(inputDate >= curDate)
        return true;
    return false;
}, "This field must be on or after current time.");

$(".broadcast-wizard").steps({
    headerTag: "h6",
    bodyTag: "section",
    transitionEffect: "fade",
    titleTemplate: '<span class="step">#index#</span> #title#',
    labels: {
        finish: "Save"
    },
    onStepChanging: function (event, currentIndex, newIndex) {
        return currentIndex > newIndex || (currentIndex < newIndex && (form.find(".body:eq(" + newIndex + ") label.error").remove(), form.find(".body:eq(" + newIndex + ") .error").removeClass("error")), form.validate().settings.ignore = ":disabled,:hidden", form.valid())
    },
    onStepChanged: function (event, currentIndex, newIndex) {
        if(currentIndex == 1) {
            var saveA = $("<a>").attr("href", "javascript:;").attr("id", "send_email").addClass("custom").text("Send Email");
            var saveB = $("<a>").attr("href", "javascript:;").attr("id", "test_email").addClass("custom").text("Test Email");
            $(document).find(".actions ul").append($("<li>").attr("aria-disabled",false).append(saveB));
            $(document).find(".actions ul").append($("<li>").attr("aria-disabled",false).append(saveA));
        } else {
            $(".actions").find(".custom").remove();
        }
    },
    onFinishing: function (event, currentIndex) {
        return form.validate().settings.ignore = ":disabled", form.valid()
    },
    onFinished: function (event, currentIndex) {
        form.find('input[name="send"]').val(0);
        form.submit();
    }
}), $(".broadcast-wizard").validate({
    ignore: "input[type=hidden], :hidden",
    errorClass: "text-danger",
    successClass: "text-success",
    highlight: function (element, errorClass) {
        $(element).removeClass(errorClass)
    },
    unhighlight: function (element, errorClass) {
        $(element).removeClass(errorClass)
    },
    errorPlacement: function (error, element, errorClass) {
        error.insertAfter(element)
    },
    rules: {
    }
});

$(document).on('click', '#send_email', function(e) {
    e.preventDefault();
    if(form.valid()) {
        form.find('input[name="send"]').val(1);
        form.submit();
        this.disabled = true;
    }
});

$(document).on('click', '#test_email', function(e) {
    e.preventDefault();
    if(form.valid()) {
        var url = document.URL, 
            shortUrl = url.split("/").splice(0, 5).join("/"),
            that = $(this);

        that.addClass('disabled');
        $.ajax({
            type: "POST",
            url: shortUrl + '/broadcasts/send',
            data: form.serialize(),
            success: function(data) {
                that.removeClass('disabled');
                if(data.success)
                    swal("Done", "We sent the email to your email address. Please enjoy.", "success");
                else
                    swal("Failed", "Failed to send email to your email address. Please try again later.", "error");
            },
            error: function (data) {
                that.removeClass('disabled');
                swal("Failed", "Unexpected error occured. Please try again later.", "error");
            },
        });
    }
});

