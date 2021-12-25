'use strict';


document.addEventListener('DOMContentLoaded', () => {

    const toggleCSSClasses = (el, ...cls) => cls.map(cl => el.classList.toggle(cl)),
        container = document.querySelector('.container'),
        menu = container.querySelector('.menu'),
        content = container.querySelector('.content'),
        menuButton = menu.querySelector('.menu__btn'),
        scrollUp = container.querySelector('.top');

    menuButton.addEventListener('click', (event) => {
        event.preventDefault();
        menu.classList.toggle('menu__active');
        content.classList.toggle('content__active');
        toggleCSSClasses(menuButton, 'menu__btn__active', 'change');
    });

    document.addEventListener('scroll', () => {
        if (window.pageYOffset > 100) {
            scrollUp.classList.add('active');
        } else {
            scrollUp.classList.remove('active');
        }
    });
});
