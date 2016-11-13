/**
 * Created by Boris on 29.10.16.
 */
$(document).ready(function () {
    var fields = ['.phone', '.name'];

    $('.callback-form').submit(function (event) {
        event.preventDefault();
        var $this = $(this);
        var id = $this.data('id');
        if (id) {
            id = '-' + id;
        } else {
            id = '';
        }
        $.each(fields, function (i, val) {
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
    $('.popup-with-form').magnificPopup({
		type: 'inline',
		preloader: false,
		focus: '#name',

		// When elemened is focused, some mobile browsers in some cases zoom in
		// It looks not nice, so we disable it:
		callbacks: {
			beforeOpen: function() {
				if($(window).width() < 700) {
					this.st.focus = false;
				} else {
					this.st.focus = '#name';
				}
			}
		}
	});
});