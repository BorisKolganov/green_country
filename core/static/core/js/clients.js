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
});
