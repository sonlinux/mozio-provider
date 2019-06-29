jQuery.validator.addMethod("domain", function(value, element) {
    return this.optional(element) || /([a-z0-9-]+\.[a-zA-Z]{2,3})/.test(value);
}, "Please specify the correct domain");

var form = $(".validation-wizard").show();

$(".validation-wizard").steps({
    headerTag: "h6",
    bodyTag: "section",
    transitionEffect: "fade",
    titleTemplate: '<span class="step">#index#</span> #title#',
    labels: {
        finish: "Register"
    },
    onStepChanging: function (event, currentIndex, newIndex) {
        return currentIndex > newIndex || (currentIndex < newIndex && (form.find(".body:eq(" + newIndex + ") label.error").remove(), form.find(".body:eq(" + newIndex + ") .error").removeClass("error")), form.validate().settings.ignore = ":disabled,:hidden", form.valid())
    },
    onFinishing: function (event, currentIndex) {
        return form.validate().settings.ignore = ":disabled", form.valid()
    },
    onFinished: function (event, currentIndex) {
        form.submit();
    }
}), $(".validation-wizard").validate({
    ignore: "input[type=hidden]",
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
        email: {
            email: !0
        },
        email2: {
            equalTo: "#id_email"
        },
        password1: {
            required: true,
            minlength: 8
        },
        password2: {
            equalTo: "#id_password1"
        },
        domain: {
            domain: true
        }
    }
});
