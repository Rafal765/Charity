document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      //this.pagination = this.$slidesContainers.querySelector(".help--slides-pagination").children;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;
      this.$currentPage = e.target.parentElement.parentElement.querySelectorAll(".btn")

      this.$currentPage.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.page === page) {
          el.classList.add("active");
        }
      });
      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */

    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation if=coś

      const form_errors = [];

      if (this.currentStep === 2) {

        let institution_types = [];
        const categories = document.querySelectorAll("input[name='categories']");
        const institutions = document.querySelectorAll("input[name='organization']");
        categories.forEach(el => {
            if (el.checked) {

            } else {
              let type = parseInt(el.value);
              institution_types.push(type)
            }
        });
        institutions.forEach(el => {
            let x = +(el.dataset.categories.split(","))
            if (institution_types.includes(x)) { //todo
              el.parentElement.parentElement.style.display = "none";
            } else {
              el.parentElement.parentElement.style.display = "block";
            }
        });
        }

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary


      if (this.currentStep === 5) {

        const bags = document.querySelector("input[name='bags']").value;
        const organization = document.querySelector("input[name='organization']").dataset.name;
        const address = document.querySelector("input[name='address']").value;
        const city = document.querySelector("input[name='city']").value;
        const postcode = document.querySelector("input[name='postcode']").value;
        if (postcode.length !== 5) {
          form_errors.push("Błędny kod pocztowy")
        }
        const phone = document.querySelector("input[name='phone']").value;
        if (phone.length !== 9) {
          form_errors.push("Błędny numer")
        }
        const data = document.querySelector("input[name='data']").value;
        const time = document.querySelector("input[name='time']").value;
        let more_info = document.querySelector("textarea[name='more_info']").value;
        if (more_info === "") {
          more_info = "Brak uwag"
        }

        const summary_bags = document.getElementById("sum_bags");
        summary_bags.innerText = bags + " worki ubrań w dobrym stanie"

        const summary_organization = document.getElementById("sum_organization");
        summary_organization.innerText = "Dla " + organization

        const summary_address = document.getElementById("sum_address");
        summary_address.innerText = address

        const summary_city = document.getElementById("sum_city");
        summary_city.innerText = city

        const summary_postcode = document.getElementById("sum_postcode");
        summary_postcode.innerText = postcode

        const summary_phone = document.getElementById("sum_phone");
        summary_phone.innerText = phone

        const summary_data = document.getElementById("sum_data");
        summary_data.innerText = data

        const summary_time = document.getElementById("sum_time");
        summary_time.innerText = time

        const summary_more_info = document.getElementById("sum_more_info");
        summary_more_info.innerText = more_info

        const my_errors = document.getElementById("errors");
        const submit_button = document.getElementById("submit");

        if (form_errors.length) {
          my_errors.innerText = "Niepoprawne wartości, proszę kliknąć 'wstecz' i dokonać poprawek";
          submit_button.style.display = "none"
        }
        else {
          submit_button.style.display = "block"
          my_errors.innerText = ""
        }
      }
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */

    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
