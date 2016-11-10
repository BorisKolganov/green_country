/**
 * Created by Boris on 29.10.16.
 */
$(document).ready(function () {
    var fields = ['.phone', '.name'];

    $('.callback-form').submit(function (event) {
        event.preventDefault();
        var $this = $(this);
        var id = $this.data('id');
        console.log(id)
        if (id) {
            id = '-' + id;
        } else {
            id = '';
        }
        $.each(fields, function (i, val) {
            console.log(val);
            console.log(val + '-' + id)
            $(val + id).removeClass('has-error');
            $(val + id + '-error').hide();
        });

        $.post($this.attr('action'), $this.serialize()).done(function (data) {
            if(data.status == 'not ok') {
                $.each(data.errors, function (key, val) {
                    $('.' + key + id).addClass('has-error');
                    $('.' + key + id + '-error').html(val);
                    $('.' + key + id + '-error').show();
                });
            } else if (data.status == 'ok') {
                $this.hide();
                $('.form-message' + id).show();
            }
        }).fail(function (data) {
            console.log(data);
        })
    })
});