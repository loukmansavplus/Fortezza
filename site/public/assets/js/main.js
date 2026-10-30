(function () {
  var d = document;

  // menu mobile
  var burger = d.querySelector('.burger'), nav = d.getElementById('nav');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      d.body.style.overflow = open ? 'hidden' : '';
      if (open && window.gsap && !d.documentElement.classList.contains('no-gsap'))
        gsap.fromTo('#nav > *', { x: 36, autoAlpha: 0 }, { x: 0, autoAlpha: 1, stagger: .06, duration: .55, delay: .1, ease: 'power3.out', clearProps: 'all' });
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); d.body.style.overflow = ''; }
    });
  }

  // pré-remplissage du service depuis ?service=
  var sel = d.getElementById('service');
  if (sel) {
    var s = new URLSearchParams(location.search).get('service');
    if (s) sel.value = s;
  }

  // formulaires : validation + envoi en AJAX (repli : envoi classique)
  d.querySelectorAll('.card-form').forEach(function (form) {
    var msg = form.querySelector('.form-msg');
    form.addEventListener('submit', function (e) {
      var bad = false;
      form.querySelectorAll('[required]').forEach(function (f) {
        var ko = f.type === 'checkbox' ? !f.checked : !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
        f.classList.toggle('bad', ko); if (ko) bad = true;
      });
      if (bad) { e.preventDefault(); msg.className = 'form-msg err'; msg.textContent = 'Merci de compléter les champs obligatoires.';
        if (window.gsap) gsap.fromTo(form, { x: -8 }, { x: 0, duration: .7, ease: 'elastic.out(1,.25)', clearProps: 'transform' }); return; }
      var file = form.querySelector('input[type=file]');
      if (file && file.files[0] && file.files[0].size > 5 * 1024 * 1024) {
        e.preventDefault(); msg.className = 'form-msg err'; msg.textContent = 'La pièce jointe dépasse 5 Mo.'; return;
      }
      if (!window.fetch) return;
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]'); btn.disabled = true;
      msg.className = 'form-msg'; msg.textContent = 'Envoi en cours…';
      var netlify = form.hasAttribute('data-netlify');
      fetch(netlify ? '/' : form.action, { method: 'POST', body: new FormData(form), headers: netlify ? {} : { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error('err'); return netlify ? { ok: true } : r.json(); })
        .then(function (j) {
          if (!j.ok) throw new Error(j.error || 'err');
          form.reset(); msg.className = 'form-msg ok'; msg.textContent = 'Merci ! Votre demande a bien été envoyée. Un accusé de réception vous a été adressé par email.';
          if (window.gsap) gsap.fromTo(msg, { y: 10, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: .6, ease: 'power3.out' });
        })
        .catch(function () { msg.className = 'form-msg err'; msg.textContent = 'L’envoi a échoué. Écrivez-nous sur WhatsApp ou par email, merci.'; })
        .then(function () { btn.disabled = false; });
    });
  });
})();
