'use strict';

$('.menu__btn').on('click', function(e) {
    e.preventDefault();
    $('.menu').toggleClass('menu__active');
    $('.content').toggleClass('content__active');
    $('.menu__btn').toggleClass('menu__btn__active');
    $('.menu__btn').toggleClass('change');
});
