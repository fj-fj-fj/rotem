// Script contains `createModal()` to create and return modal window,
// `viewModal()` to show popup window with Rotem-test-options.


/* #region CreateModal */

/**
 * Create modal object.
 * 
 * @param {string} options - options for popup window
 * @returns modal-window object with open(), close() and setContent() actions
*/
const createModal = function(options) {
    /** Create and return popup window (HTMLDivElement). */
    function _createModalElement(options) {
        const DEFAULT_TITLE = '';
        const DEFAULT_CONTENT = '';
        const _modal = document.createElement('div');
        _modal.classList.add('modal');
        _modal.insertAdjacentHTML('afterbegin',
            `<div class='modal__overlay' data-close='true'>
                <div class='modal__window' ${options.showFooter || "style='justify-content:space-evenly;'"}>
                    <div class='modal__header'>
                        <span class='modal__title'>${options.title || DEFAULT_TITLE}</span>
                        ${options.closable ? `
                            <span class='modal__close' data-close='true' style='--hover-color:${options.color};'>
                                &times;
                            </span>` : false
                        }
                    </div>
                    <div class='modal__body' data-content>
                        ${options.content || DEFAULT_CONTENT}
                    </div>
                    ${options.showFooter && `
                        <div class='modal__footer'>
                            <button>Ага, ясно</button>
                            <button>Почитать еще</button>
                        </div>` || ''
                    }
                </div>
            </div>`
        );
        document.body.appendChild(_modal);
        return _modal;
    }

    const ANIMATION_SPED = 200;
    const modalElement = _createModalElement(options);
    let closing = false;

    // Object with open(), close() and setContent()
    const modal = {
        open() {
            /*jshint expr:true*/
            !closing && modalElement.classList.add('open'); // -W030
        },
        close() {
            closing = true;
            modalElement.classList.remove('open');
            modalElement.classList.add('hiden');
            setTimeout(() => {
                modalElement.classList.remove('hiden');
                closing = false;
                },
                ANIMATION_SPED
            );
        },
        setContent(html) {
            modalElement.querySelector('[data-content]').innerHTML = html;
        }
    };

    // Close window if clicked 'X' or background
    const closeModal = event => {
        console.log('clicked', event.target.dataset.close);
        if (event.target.dataset.close) {
            modal.close();
        }
    };
    modalElement.addEventListener('click', closeModal);

    return modal;
};

/* #endregion CreateModal */


/* #region ViewModal */


/**
 * Show popup window with Rotem-test-options.
 * 
 * @param {boolean} closable - show close-button or not
 * @param {boolean} showFooter - show footer or not
 */
const viewModal = function(closable = true, showFooter = false) {
    function _showModalByClickedButton() {
        document.querySelector('.modal__intem').addEventListener('click', () => {
            const COLOR = '#0055BE';
            const testIntem = {
                closable: closable,
                showFooter: showFooter,
                title: `<span style='color:${COLOR};'>INTEM</span>`,
                content: `При проведении <span style='color:${COLOR};'>INTEM</span>-теста \
                    в качестве контактного активатора внутреннего пути коагуляции используют \
                    эллаговую кислоту. Тест чувствителен к дефициту факторов свертывания \
                    крови, формирующих внутренний путь коагуляции.<br>При помощи параметров \
                    <span style='color:${COLOR};'>INTEM</span>-теста может быть исследован \
                    весь гемостаз через активацию, формирование, полимеризацию, устойчивость \
                    сгустков и фибринолиз, а также ингибицию каскада формирования сгустков \
                    высокими дозами антикоагулянтов, антифибринолитиков, из-за дефектов \
                    полимеризации фибрина или гиперфибринолиза, дефицита фибрина, \
                    тромбоцитопении и нарушений функций тромбоцитов. Величины параметров, \
                    выходящие за пределы установленных контрольных диапазонов, сигнализируют \
                    о возможном неправильном протекании коагуляции.`,
                color: COLOR
            };
            createModal(testIntem).open();
        });
        document.querySelector('.modal__extem').addEventListener('click', () => {
            const COLOR = '#DF2633';
            const testExtem = {
                closable: closable,
                showFooter: showFooter,
                title: `<span style='color:${COLOR};'>EXTEM</span>`,
                content: `<span style='color:${COLOR};'>EXTEM</span> – основной тест, при \
                    котором для активации внешнего пути коагуляции используется \
                    рекомбинантный тканевой фактор. При определении параметров свертывания крови \
                    с помощью <span style='color:${COLOR};'>EXTEM</span>-теста \
                    представляется информация и о первичной активации и \
                    динамике образования сгустка, позволяя выявить проявления \
                    недостаточности факторов свертывания крови (внешнего пути). Выходящие за \
                    пределы нормы результаты в тесте <span style='color:${COLOR};'>EXTEM</span> \
                    могут быть вызваны действием антикоагулянтов, таких как гирудин и \
                    других прямых ингибиторов тромбина. Оральные антикоагулянты \
                    (кумарин) оказывают второстепенное влияние на результаты в \
                    сравнении с протромбиновым временем. Значительно повышенный \
                    или пониженный гематокрит может повлиять на результаты \
                    тромбоэластометрических измерений.`,
                color: COLOR
            };
            createModal(testExtem).open();
        });
        document.querySelector('.modal__heptem').addEventListener('click', () => {
            const COLOR = '#8A949C';
            const testHeptem = {
                closable: closable,
                showFooter: showFooter,
                title: `<span style='color:${COLOR};'>HEPTEM</span>`,
                content: `<span style='color:${COLOR};'>HEPTEM</span>-тест представляет \
                    собой анализ <span style='color:#0055BE;'>INTEM</span>, выполняемый \
                    в присутствии гепариназы, инактивирующей гепарин in vitro, в результате \
                    чего гепарин теряет свои антикоагуляционные свойства. \
                    Это позволяет выявить нарушения гемостаза даже в присутствии \
                    гепарина и определяет специфическое действие антикоагулянтов.`,
                color: COLOR
            };
            createModal(testHeptem).open();
        });
        document.querySelector('.modal__fibtem').addEventListener('click', () => {
            const COLOR = '#7F2C12';
            const testFibtem = {
                closable: closable,
                showFooter: showFooter,
                title: `<span style='color:${COLOR};'>FIBTEM</span>`,
                content: `В тесте <span style='color:${COLOR};'>INTEM</span> активность \
                    тромбоцитов подавляется цитохалазином D, сильным ингибитором \
                    полимеризации актина, который разрушает актин микрофиламентов, существенную \
                    часть цитоскелет-опосредованной стягиваемости тромбоцитов. \
                    <span style='color:${COLOR};'>INTEM</span> устраняет влияние \
                    тромбоцитов на тромбообразование и позволяет обнаруживать дефицит \
                    фибриногена или качественные нарушения полимеризации фибрина. Неустойчивые \
                    сгустки фибрина в тесте <span style='color:${COLOR};'>INTEM</span> указывают \
                    на нехватку фибриногена или нарушения в процессе полимеризации фибрина.`,
                color: COLOR
            };
            createModal(testFibtem).open();
        });
        document.querySelector('.modal__aptem').addEventListener('click', () => {
            const COLOR = '#683274';
            const testApem = {
                closable: closable,
                showFooter: showFooter,
                title: `<span style='color:${COLOR};'>APTEM</span>`,
                content: `Тест <span style='color:${COLOR};'>APTEM</span> выполняется на \
                    основе анализа <span style='color:#DF2633;'>EXTEM</span>, в котором \
                    фибринолиз подавляется апротинином (антагонист плазмина). \
                    Сравнение результатов <span style='color:${COLOR};'>APTEM</span> и \
                    <span style='color:#DF2633;'>EXTEM</span> тестов позволяет выявить \
                    гиперфибринолиз и обосновать необходимость назначения \
                    антифибринолитических средств, что практически невозможно \
                    установить классическими лабораторными тестами.`,
                color: COLOR
            };
            createModal(testApem).open();
        });
    }
    _showModalByClickedButton();
};

/* #endregion ViewModal */

viewModal();
