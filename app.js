/* app.js — Floor Cleaning Squad premium interactions */
(function () {
  'use strict';

  /* ---- Mark JS as active (enables reveal opacity:0 hide) ---- */
  document.documentElement.classList.add('js-on');

  /* ---- Navbar scroll ---- */
  const nav = document.getElementById('navbar');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });
  }

  /* ---- Mobile hamburger ---- */
  const ham = document.querySelector('.hamburger');
  const mobileNav = document.querySelector('.mobile-nav');
  if (ham && mobileNav) {
    ham.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
    });
  }

  /* ---- Scroll reveal ---- */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const revealObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          revealObs.unobserve(e.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px 0px 0px' });
    revealEls.forEach(el => revealObs.observe(el));
  }

  /* ---- Counter animation ---- */
  const counters = document.querySelectorAll('.counter');
  if (counters.length) {
    const countObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;

        const el = e.target;
        const target = parseInt(el.dataset.to, 10);
        const suffix = el.dataset.suffix || '';
        let start = null;
        const duration = 2000;
        const step = ts => {
          if (!start) start = ts;
          const prog = Math.min((ts - start) / duration, 1);
          const ease = 1 - Math.pow(1 - prog, 3);
          el.textContent = Math.floor(ease * target).toLocaleString() + suffix;
          if (prog < 1) requestAnimationFrame(step);
          else el.textContent = target.toLocaleString() + suffix;
        };
        requestAnimationFrame(step);
        countObs.unobserve(el);
      });
    }, { threshold: 0.1 });
    counters.forEach(c => countObs.observe(c));
  }

  /* ---- Button ripple ---- */
  document.querySelectorAll('.btn-primary, .btn-outline, .btn-secondary, .btn-nav').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const rect = btn.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const r = document.createElement('span');
      r.className = 'ripple';
      r.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX-rect.left-size/2}px;top:${e.clientY-rect.top-size/2}px`;
      btn.appendChild(r);
      r.addEventListener('animationend', () => r.remove());
    });
  });

  /* ---- Hero sparkle canvas ---- */
  const canvas = document.getElementById('sparkle-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let W, H;
    function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
    resize();
    window.addEventListener('resize', resize, { passive: true });
    const particles = [];
    let mx = -999, my = -999;
    window.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; }, { passive: true });
    function loop() {
      ctx.clearRect(0, 0, W, H);
      if (mx > 0 && my > 0 && my < H * 0.85) {
        for (let i = 0; i < 2; i++) {
          particles.push({
            x: mx + (Math.random() - 0.5) * 14,
            y: my + (Math.random() - 0.5) * 14,
            vx: (Math.random() - 0.5) * 1.2,
            vy: -Math.random() * 2 - 0.3,
            life: 1,
            size: Math.random() * 3 + 1.5,
            hue: Math.random() * 40 + 140  // greens/teals
          });
        }
      }
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx; p.y += p.vy; p.vy += 0.035; p.life -= 0.022;
        if (p.life <= 0) { particles.splice(i, 1); continue; }
        ctx.save();
        ctx.globalAlpha = p.life * 0.75;
        ctx.fillStyle = `hsl(${p.hue},90%,60%)`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
      requestAnimationFrame(loop);
    }
    loop();
  }

  /* ---- Quote form handler ---- */
  const form = document.getElementById('quote-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const success = document.getElementById('form-success');
      if (success) {
        form.style.display = 'none';
        success.style.display = 'block';
      }
    });
  }

}());
