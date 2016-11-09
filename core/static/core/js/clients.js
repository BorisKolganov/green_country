$(document).ready(function () {
   $('.clients').slick({
        slidesToShow: 5,
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
    var map;
    ymaps.ready(function () {
        map =  new ymaps.Map("map", {
            center: [55.76, 37.64],
            zoom: 11
        });
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
