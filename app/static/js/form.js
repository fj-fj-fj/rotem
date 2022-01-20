// interpretation-of-results page
// Script contain `callAjax()` and sending data to server side
'use strict';


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


/** @type {Element} */
const testCategories = document.querySelector('.results_interpretation__categories');

if (testCategories) {
    [...testCategories.children].forEach(/** @type Element */ btn => {

        // Check localStorage and set values if exists
        const formStorage = localStorage.getItem('form');
        if (formStorage) {
            let form = document.querySelector(`#${formStorage}.form-contact`);
            form.style.display = "block";
        }

        btn.addEventListener('click', event => {

            // Send to server clicked-category-button (<obsteric|surgery|covid>_category)
            callAjax(btn.id);

            // Delete flash message
            let flashMessage = document.querySelector('.flash.error, .flash.success');
            if (flashMessage) {flashMessage.remove();}

            // Show form (form_<obsteric|surgery|covid>) based on clicked-category-button
            let forms = document.querySelectorAll('.form-contact');
            if (btn.id === "obsteric_category") {
                forms.forEach(/** @type Element */ form => {
                    if (form.id == "form_obsteric") {
                        form.style.display = "block";
                        localStorage.setItem('form', form.id);
                    } else {
                        form.style.display = "none";
                    }
                });
            } else if (btn.id === "surgery_category") {
                forms.forEach(/** @type Element */ form => {
                    if (form.id == "form_surgery") {
                        form.style.display = "block";
                        localStorage.setItem('form', form.id);
                    } else {
                        form.style.display = "none";
                    }
                });
            } else if (btn.id === "covid_category") {
                forms.forEach(/** @type Element */ form => {
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
