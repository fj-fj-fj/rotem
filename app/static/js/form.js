/**
 * interpretation-of-results page.
 * See {@link ../../templates/result_interpretation.html}
 *
 * @module form
 */

"use strict";


/**
 * Send data to server side.
 *
 * @param {String} category - clicked category button
 */
function callAjax(category) {
  const clickedCategoryBtn = JSON.stringify({
    "clicked_category_button": category
  });
  const request = new XMLHttpRequest();
  request.open("POST", "/interpretation-of-results", true);
  request.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded; charset=UTF-8"
  );
  request.send(clickedCategoryBtn);
}


/**
 * Enum category-button values.
 * @enum {String}
 */
const testCategory = Object.freeze({
  OBSTERIC: "obsteric_category",
  SURGERY: "surgery_category",
  COVID: "covid_category"
});


/**
 * Enum form-category values.
 * @enum {string}
 */
const formCategory = Object.freeze({
  OBSTERIC: "form_obsteric",
  SURGERY: "form_surgery",
  COVID: "form_covid"
});


/**
 * Display form, set focus and save form.id to local storage.
 *
 * @param {Element} form - one of the page forms
 */
function _displayFocusFreezeForm(form) {
  form.style.display = "block";
  form.scrollIntoView({block: "center", behavior: "smooth"});
  localStorage.setItem("form", form.id);
}


/** @type {Element|null} isCategoryBtns - /interpretation-of-the-result page is loaded or not */
const isCategoryBtns = document.querySelector(".results_interpretation__categories");

if (isCategoryBtns) {

  /** @type {String} */
  const flashErrorOrSuccess = ".flash.error, .flash.success";

  [...isCategoryBtns.children].forEach(/** @type {Element} */ btn => {

    /**
     * Check `localStorage` and set values if exists
     * @type {Enumeratiion} formStorage - one of the `formCategory` values
     * @type {Element} form - form to be displayed on the page
     * */
    const formStorage = localStorage.getItem("form");
    if (formStorage) {
        let form = document.querySelector(`#${formStorage}.form-contact`);
        form.style.display = "block";
    }

    btn.addEventListener("click", () => {

      /**
       * Send clicked button to server side.
       * @typedef {Enumeratiion} btn.id one of the `testCategory` values
       */
      callAjax(btn.id);

      /**
       * Delete the flash message.
       * @type {Element|null} flashMessage - flash messages are on the page or not
       * */
      let flashMessage = document.querySelector(flashErrorOrSuccess);
      if (flashMessage) {flashMessage.remove();}

      /**
       * @type {NodeListOf<Element>} forms - all page forms
       * */
      let forms = document.querySelectorAll(".form-contact");

      /** Display the form, depending on the category and set the focus for it. */
      if (btn.id === testCategory.OBSTERIC) {
        forms.forEach(/** @type {Element} */ form => {
          if (form.id == formCategory.OBSTERIC) {
            _displayFocusFreezeForm(form);
          } else {
            form.style.display = "none";
          }
        });
      } else if (btn.id === testCategory.SURGERY) {
        forms.forEach(/** @type Element */ form => {
          if (form.id == formCategory.SURGERY) {
            _displayFocusFreezeForm(form);
          } else {
            form.style.display = "none";
          }
        });
      } else if (btn.id === testCategory.COVID) {
        forms.forEach(/** @type Element */ form => {
          if (form.id == formCategory.COVID) {
            _displayFocusFreezeForm(form);
          } else {
            form.style.display = "none";
          }
        });
      }

      /** Set the values to local storage. See also {@link _displayFocusFreezeForm} */
      localStorage.setItem("display", "block");
      // If the user reopens the window or tab, display the set values.
      // The values ​​will be cleared when the user leaves the page.
      // (main.js checks if /interpretation-of-the-result page is loaded
      // and if not, clears form/display pairs.).

    });
  });

  /**
   * Set focus on the flash messages.
   * @type {Element|null} flashMessage - flash messages are on the page or not
   * */
  let flashMessage = document.querySelector(flashErrorOrSuccess);
  if (flashMessage) { flashMessage.scrollIntoView(); }
}
