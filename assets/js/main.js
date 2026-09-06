/* Torres Cleaning Services — homepage mockup behaviour.
   Vanilla JS, no dependencies. Everything here degrades gracefully:
   with JS off the page is still fully readable and navigable. */

(function () {
  'use strict';

  /* ------------------------------ Mobile nav ----------------------------- */

  var toggle = document.querySelector('.nav-toggle');
  var nav    = document.getElementById('primary-nav');

  if (toggle && nav) {
    var mq = window.matchMedia('(max-width: 980px)');

    var setNav = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      nav.hidden = !open;
    };

    // The nav is a plain flex row on desktop and a dropdown below 980px, so
    // sync `hidden` to the breakpoint rather than to the toggle alone.
    var syncToBreakpoint = function () {
      if (mq.matches) { setNav(false); } else { nav.hidden = false; toggle.setAttribute('aria-expanded', 'false'); }
    };

    syncToBreakpoint();
    mq.addEventListener('change', syncToBreakpoint);

    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', function (e) {
      if (mq.matches && e.target.closest('a')) { setNav(false); }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mq.matches && toggle.getAttribute('aria-expanded') === 'true') {
        setNav(false);
        toggle.focus();
      }
    });
  }

  /* ---------------------------- Footer year ------------------------------ */

  var year = document.getElementById('year');
  if (year) { year.textContent = String(new Date().getFullYear()); }

  /* -------------------------- Estimate form ------------------------------ */
  /* Mockup only — nothing is sent anywhere. Wire the submit handler to a real
     endpoint (Formspree, Netlify Forms, your CRM) before launch. */

  var form   = document.getElementById('estimate-form');
  var status = document.getElementById('form-status');

  if (form && status) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var name  = form.elements.name.value.trim();
      var phone = form.elements.phone.value.trim();

      if (!name || !phone) {
        status.hidden = false;
        status.textContent = 'Please add your name and a phone number so we can reach you.';
        (name ? form.elements.phone : form.elements.name).focus();
        return;
      }

      status.hidden = false;
      status.textContent =
        'Thanks, ' + name + ' — this is a mockup, so nothing was actually sent. ' +
        'Connect this form to a real endpoint before launch.';
      status.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
  }

  /* --------------------- Placeholder highlighting ------------------------ */
  /* Every bit of copy still waiting on a real business detail is marked with
     .ph. This toggle makes them all visible so nothing ships unfilled.
     Delete the .ph-bar element (and this block) before launch. */

  var phToggle = document.getElementById('ph-toggle');
  var phCount  = document.getElementById('ph-count');
  var marks    = document.querySelectorAll('.ph');

  if (phCount) { phCount.textContent = String(marks.length); }

  if (phToggle) {
    var KEY = 'tcs-show-placeholders';
    var stored;
    try { stored = window.localStorage.getItem(KEY); } catch (err) { stored = null; }

    var apply = function (on) {
      document.body.classList.toggle('show-ph', on);
      phToggle.checked = on;
      try { window.localStorage.setItem(KEY, on ? '1' : '0'); } catch (err) { /* private mode */ }
    };

    apply(stored === '1');
    phToggle.addEventListener('change', function () { apply(phToggle.checked); });
  }
})();
