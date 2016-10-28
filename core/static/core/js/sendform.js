/**
 * Created by Boris on 29.10.16.
 */
$(document).ready(function () {
    var fields = ['.phone', '.name'];

    $('.callback-form').submit(function (event) {
        event.preventDefault();
        var $this = $(this);
        $.each(fields, function (i, val) {
            $(val).removeClass('has-error');
            $(val + '-error').hide();
        });

        $.post($this.attr('action'), $this.serialize()).done(function (data) {
            if(data.status == 'not ok') {
                $.each(data.errors, function (key, val) {
                    $('.' + key).addClass('has-error');
                    $('.' + key + '-error').html(val);
                    $('.' + key + '-error').show();
                });
            } else if (data.status == 'ok') {
                $this.hide();
                $('.form-message').show();
            }
        }).fail(function (data) {
            console.log(data);
        })
    })
});