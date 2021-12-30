'use strict';


document.addEventListener('DOMContentLoaded', () => {

    const container = document.querySelector('.container'),
        menu = container.querySelector('.menu'),
        content = container.querySelector('.content'),
        menuButton = menu.querySelector('.menu__btn'),
        scrollUp = container.querySelector('.top'),
        breadcrumb = container.querySelector('.breadcrumb a');
    
    function toggleCSSClasses(el, ...cls) {
        cls.map(cl => el.classList.toggle(cl));
    }

    function openMenu(event) {
        event.preventDefault();
        menu.classList.toggle('menu__active');
        content.classList.toggle('content__active');
        toggleCSSClasses(menuButton, 'menu__btn__active', 'change');
    }

    menuButton.addEventListener('click', (event) => openMenu(event));

    document.addEventListener('scroll', () => {
        if (window.pageYOffset > 100) {
            scrollUp.classList.add('active');
        } else {
            scrollUp.classList.remove('active');
        }
    });

    if (breadcrumb.text === 'меню') {
        breadcrumb.addEventListener('click', (event) => openMenu(event));
    } else {
        breadcrumb.parentElement.innerHTML = '';
    }
});
