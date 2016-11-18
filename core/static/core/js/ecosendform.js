/**
 * Created by Boris on 29.10.16.
 */
$(document).ready(function () {
    var fields = ['.phone', '.name', '.email', '.org'];

    $('.eco-form').submit(function (event) {
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
    
    $('.photos').slick({
        slidesToShow: 4,
        infinite: true,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    arrows: false,
                    centerMode: true,
                    // centerPadding: '4 0px',
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 480,
                settings: {
                    arrows: false,
                    centerMode: true,
                    // centerPadding: '40px',
                    slidesToShow: 1
                }
            }
        ],
        autoplay: true,
        autoplaySpeed: 2000
    });
});