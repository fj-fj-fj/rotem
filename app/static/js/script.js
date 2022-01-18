'use strict';


document.addEventListener('DOMContentLoaded', () => {

    const container = document.querySelector('.container'),
        menu = container.querySelector('.menu'),
        content = container.querySelector('.content'),
        menuButton = menu.querySelector('.menu__btn'),
        scrollUp = container.querySelector('.top'),
        breadcrumb = container.querySelector('.breadcrumb a'),
        testCategories = container.querySelector('.results_interpretation__categories');
    
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

    /**
     * Send data to server side.
     * 
     * @param {string} category - clicked category button
     */
    function callAjax(category) {
        const clickedCategoryBtn = JSON.stringify({
            'clicked_category_button': category
        });
        const request = new XMLHttpRequest();
        request.open('POST', '/interpretation-of-results', true);
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        request.send(clickedCategoryBtn);
    }

    // interpretation-of-results page
    if (testCategories) {
        [...testCategories.children].forEach(/** @type string */ item => {

            // Check localStorage and set values if exists
            const formStorage = localStorage.getItem('form');
            if (formStorage) {
                let form = document.querySelector(`#${formStorage}.form-contact`);
                form.style.display = "block";
            }

            item.addEventListener('click', event => {

                // Send to server clicked-category-button (<obsteric|surgery|covid>_category)
                callAjax(item.id);

                // Delete flash message
                let flashMessage = document.querySelector('.flash.error, .flash.success');
                if (flashMessage) {flashMessage.remove();}

                // Show form (form_<obsteric|surgery|covid>) based on clicked-category-button
                let forms = document.querySelectorAll('.form-contact');
                if (item.id === "obsteric_category") {
                    forms.forEach(form => {
                        if (form.id == "form_obsteric") {
                            form.style.display = "block";
                            localStorage.setItem('form', form.id);
                        } else {
                            form.style.display = "none";
                        }
                    });
                } else if (item.id === "surgery_category") {
                    forms.forEach(form => {
                        if (form.id == "form_surgery") {
                            form.style.display = "block";
                            localStorage.setItem('form', form.id);
                        } else {
                            form.style.display = "none";
                        }
                    });
                } else if (item.id === "covid_category") {
                    forms.forEach(form => {
                        if (form.id == "form_covid") {
                            form.style.display = "block";
                            localStorage.setItem('form', form.id);
                        } else {
                            form.style.display = "none";
                        }
                    });
                }
            localStorage.setItem('display', 'block');
            });
        });
    } else {
        // Remove values if user closed page
        localStorage.removeItem('form');
    }
});
