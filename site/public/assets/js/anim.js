/* Animations Fortezza : GSAP + ScrollTrigger (amélioration progressive) */
(function () {
  var d = document, html = d.documentElement;
  if (!window.gsap || !window.ScrollTrigger || html.classList.contains('no-gsap')) return;
  // « Réduire les animations » (Windows/macOS) : version douce (fondus seuls), ajouter ?anim=full à l'URL pour tout voir
  var soft = matchMedia('(prefers-reduced-motion: reduce)').matches && !/anim=full/.test(location.search);
  if (soft) html.classList.add('soft');

  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: 'power3.out' });
  var $ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  /* ---- découpe d'un titre en mots (conserve <em>) ---- */
  function split(el) {
    if (el.dataset.split) return $('.wi', el);
    el.dataset.split = 1;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var f = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (t) {
            if (!t) return;
            if (/^\s+$/.test(t)) { f.appendChild(d.createTextNode(' ')); return; }
            var w = d.createElement('span'), i = d.createElement('span');
            w.className = 'w'; i.className = 'wi'; i.textContent = t; w.appendChild(i); f.appendChild(w);
          });
          node.replaceChild(f, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    })(el);
    el.classList.add('split-done');
    return $('.wi', el);
  }

  /* ---- 1. intro du hero (accueil + pages internes) ---- */
  var hero = d.querySelector('.hero, .page-hero');
  if (hero) {
    var tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
    var words = split(hero.querySelector('h1'));
    var eb = hero.querySelector('.eyebrow'), lead = hero.querySelector('.lead');
    gsap.set(words, soft ? { autoAlpha: 0 } : { yPercent: 118, rotate: 4 });
    tl.fromTo($('.crumbs', hero), { autoAlpha: 0, y: 12 }, { autoAlpha: 1, y: 0, duration: .7 }, 0)
      .fromTo(eb, { autoAlpha: 0, x: -24 }, { autoAlpha: 1, x: 0, duration: .8 }, .1)
      .fromTo(eb, { '--ln': 0 }, { '--ln': 1, duration: .9 }, .15)
      .to(words, soft ? { autoAlpha: 1, duration: .9, stagger: .05 } : { yPercent: 0, rotate: 0, duration: 1.15, stagger: .07 }, .25)
      .fromTo(lead, { autoAlpha: 0, y: soft ? 8 : 26 }, { autoAlpha: 1, y: 0, duration: .9 }, .8)
      .fromTo($('.hero-btns .btn', hero), { autoAlpha: 0, y: 26, scale: .94 }, { autoAlpha: 1, y: 0, scale: 1, duration: .8, stagger: .1 }, .95)
      .fromTo($('.hero-proof li', hero), { autoAlpha: 0, y: 22 }, { autoAlpha: 1, y: 0, duration: .8, stagger: .09 }, 1.1);
    var bgImg = hero.querySelector('.hero-bg img, .ph-bg img');
    if (bgImg && !soft) gsap.fromTo(bgImg, { scale: 1.2 }, { scale: 1.02, duration: 2.4, ease: 'power2.out' });
    var bg = hero.querySelector('.hero-bg, .ph-bg');
    if (bg && !soft) gsap.to(bg, { yPercent: 14, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
  }

  /* ---- 2. blocs de texte : eyebrow, titre mot par mot, paragraphes ---- */
  $('.sec-head, .split-txt, .txtblock').forEach(function (b) {
    b.classList.remove('reveal'); gsap.set(b, { opacity: 1 });
    var t = 0, tl = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
    Array.prototype.slice.call(b.children).forEach(function (k) {
      if (k.tagName === 'H2') {
        var w = split(k); gsap.set(w, soft ? { autoAlpha: 0 } : { yPercent: 118, rotate: 3 });
        tl.to(w, soft ? { autoAlpha: 1, duration: .8, stagger: .04 } : { yPercent: 0, rotate: 0, duration: 1, stagger: .055 }, t); t += .12;
      } else if (k.classList.contains('eyebrow')) {
        gsap.set(k, { autoAlpha: 0, x: -18, '--ln': 0 });
        tl.to(k, { autoAlpha: 1, x: 0, duration: .7 }, t).to(k, { '--ln': 1, duration: .8 }, t);
      } else {
        gsap.set(k, { autoAlpha: 0, y: soft ? 8 : 28 });
        tl.to(k, { autoAlpha: 1, y: 0, duration: .85 }, t + .18); t += .12;
      }
    });
    ScrollTrigger.create({ trigger: b, start: 'top 84%', once: true, onEnter: function () { tl.play(); } });
  });

  /* ---- 3. images éditoriales : révélation par masque + carte flottante ---- */
  $('.split-img').forEach(function (box) {
    box.classList.remove('reveal');
    var img = $('img', box)[0], card = $('.float-card', box)[0];
    gsap.set(img, soft ? { autoAlpha: 0 } : { clipPath: 'inset(0 0 100% 0 round 14px)', scale: 1.18 });
    if (card) gsap.set(card, { autoAlpha: 0, y: 40, scale: .92 });
    ScrollTrigger.create({
      trigger: box, start: 'top 85%', once: true, onEnter: function () {
        gsap.to(img, soft ? { autoAlpha: 1, duration: 1 } : { clipPath: 'inset(0 0 0% 0 round 14px)', scale: 1, duration: 1.4, ease: 'power4.out', clearProps: 'clipPath,transform' });
        if (card) gsap.to(card, { autoAlpha: 1, y: 0, scale: 1, duration: .9, delay: .7, ease: 'back.out(1.6)' });
      }
    });
  });

  /* ---- 4. cartes (pôles, pourquoi, formulaires…) ---- */
  ScrollTrigger.batch('.reveal', {
    start: 'top 90%', once: true,
    onEnter: function (els) {
      gsap.fromTo(els, { autoAlpha: 0, y: soft ? 14 : 56 }, { autoAlpha: 1, y: 0, duration: .95, stagger: .13, overwrite: true, clearProps: 'transform' });
    }
  });

  $('.pole-card').forEach(function (c) {
    var img = $('.pc-img img', c)[0], num = $('.pc-num', c)[0], ic = $('.pc-ic', c)[0];
    if (soft) return;
    gsap.set(img, { scale: 1.3 }); gsap.set(num, { xPercent: -100 }); gsap.set(ic, { scale: 0, rotate: -40 });
    ScrollTrigger.create({
      trigger: c, start: 'top 88%', once: true, onEnter: function () {
        gsap.to(img, { scale: 1, duration: 1.6, ease: 'power3.out', clearProps: 'transform' });
        gsap.to(num, { xPercent: 0, duration: .7, delay: .25, ease: 'power4.out' });
        gsap.to(ic, { scale: 1, rotate: 0, duration: .8, delay: .4, ease: 'back.out(2.2)', clearProps: 'transform' });
      }
    });
  });

  $('.why-card .ic').forEach(function (ic) {
    if (soft) return;
    gsap.set(ic, { scale: 0, rotate: -30 });
    ScrollTrigger.create({ trigger: ic, start: 'top 90%', once: true, onEnter: function () {
      gsap.to(ic, { scale: 1, rotate: 0, duration: .8, delay: .35, ease: 'back.out(2.4)' });
    } });
  });

  $('.presta li').forEach(function (li) { li.classList.remove('reveal'); });
  var pli = $('.presta li');
  if (pli.length) {
    gsap.set(pli, { autoAlpha: 0, x: soft ? 0 : -34 });
    ScrollTrigger.create({ trigger: '.presta', start: 'top 80%', once: true, onEnter: function () {
      gsap.to(pli, { autoAlpha: 1, x: 0, duration: .8, stagger: .13, delay: .2 });
      if (!soft) gsap.fromTo($('.presta .n'), { scale: 0 }, { scale: 1, duration: .6, stagger: .13, delay: .45, ease: 'back.out(2.4)' });
    } });
  }

  $('.card-form').forEach(function (f) {
    var kids = Array.prototype.slice.call(f.children).filter(function (k) { return !k.classList.contains('hp') && k.type !== 'hidden'; });
    gsap.set(kids, { autoAlpha: 0, y: 18 });
    ScrollTrigger.create({ trigger: f, start: 'top 82%', once: true, onEnter: function () {
      gsap.to(kids, { autoAlpha: 1, y: 0, duration: .7, stagger: .07, delay: .2 });
    } });
  });

  var fcols = $('.foot-grid > div');
  gsap.set(fcols, { autoAlpha: 0, y: 30 });
  ScrollTrigger.create({ trigger: '.site-footer', start: 'top 92%', once: true, onEnter: function () {
    gsap.to(fcols, { autoAlpha: 1, y: 0, duration: .8, stagger: .1 });
  } });

  /* ---- 5. header : ombre, compact, se masque en descendant ---- */
  var hdr = d.querySelector('.site-header'), nav = d.getElementById('nav');
  if (!soft) ScrollTrigger.create({
    start: 0, end: 'max', onUpdate: function (s) {
      var y = s.scroll();
      hdr.classList.toggle('scrolled', y > 20);
      if (y > 520 && s.direction === 1 && !nav.classList.contains('open')) hdr.classList.add('hide');
      else if (s.direction === -1 || y <= 520) hdr.classList.remove('hide');
    }
  });

  /* ---- 6. barre de progression ---- */
  if (!soft) { var bar = d.createElement('div'); bar.className = 'progress'; bar.setAttribute('aria-hidden', 'true'); d.body.appendChild(bar);
  gsap.to(bar, { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: .25 } }); }

  /* ---- 7. interactions souris : boutons magnétiques + halo des cartes ---- */
  if (!soft && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    $('.btn, .wa-float').forEach(function (el) {
      el.classList.add('is-mag');
      var xT = gsap.quickTo(el, 'x', { duration: .5, ease: 'power3' }), yT = gsap.quickTo(el, 'y', { duration: .5, ease: 'power3' });
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        xT((e.clientX - r.left - r.width / 2) * .22); yT((e.clientY - r.top - r.height / 2) * .3 - 2);
      });
      el.addEventListener('mouseleave', function () { xT(0); yT(0); });
    });
    $('.why-card').forEach(function (c) {
      c.addEventListener('mousemove', function (e) {
        var r = c.getBoundingClientRect();
        c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
