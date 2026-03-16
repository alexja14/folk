(function () {
    'use strict';

    /* ---- 1. Button Ripple Effect ---- */
    function attachRipple(btn) {
        btn.addEventListener('click', function (e) {
            const rect = btn.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            const ripple = document.createElement('span');
            ripple.className = 'bellissimo-ripple';
            ripple.style.cssText = `width:${size}px;height:${size}px;left:${x}px;top:${y}px`;
            btn.appendChild(ripple);
            ripple.addEventListener('animationend', () => ripple.remove());
        });
    }

    /* ---- 2. Navbar scroll background ---- */
    function initNavScroll() {
        const nav = document.querySelector('.elementor-nav-menu--main, .site-header, header');
        if (!nav) return;
        window.addEventListener('scroll', () => {
            nav.classList.toggle('bellissimo-nav-scrolled', window.scrollY > 60);
        }, { passive: true });
    }

    /* ---- 3. Cursor sparkle canvas ---- */
    function initSparkles() {
        const canvas = document.createElement('canvas');
        canvas.id = 'bellissimo-canvas';
        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        let W = canvas.width = window.innerWidth;
        let H = canvas.height = window.innerHeight;
        window.addEventListener('resize', () => {
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
        });

        const particles = [];
        let mx = -999, my = -999;

        window.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; }, { passive: true });

        function spawn() {
            if (mx < 0) return;
            for (let i = 0; i < 2; i++) {
                particles.push({
                    x: mx + (Math.random() - 0.5) * 12,
                    y: my + (Math.random() - 0.5) * 12,
                    vx: (Math.random() - 0.5) * 1.5,
                    vy: -Math.random() * 2 - 0.5,
                    life: 1,
                    size: Math.random() * 4 + 2,
                    hue: Math.random() * 60 + 20   // golds / oranges
                });
            }
        }

        function loop() {
            ctx.clearRect(0, 0, W, H);
            spawn();
            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.vy += 0.04;  // gentle gravity
                p.life -= 0.025;
                if (p.life <= 0) { particles.splice(i, 1); continue; }
                ctx.save();
                ctx.globalAlpha = p.life * 0.8;
                ctx.fillStyle = `hsl(${p.hue}, 100%, 65%)`;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
            requestAnimationFrame(loop);
        }
        loop();
    }

    /* ---- 4. Smooth counter animation for numbers ---- */
    function animateCounters() {
        const numberEls = document.querySelectorAll(
            '.elementor-counter-number, [data-to], .e-counter'
        );
        if (!numberEls.length) return;
        const obs = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const target = parseInt(el.getAttribute('data-to') || el.innerText.replace(/\D/g, ''), 10);
                if (isNaN(target)) return;
                let start = 0;
                const duration = 1800;
                const step = timestamp => {
                    if (!start) start = timestamp;
                    const progress = Math.min((timestamp - start) / duration, 1);
                    const ease = 1 - Math.pow(1 - progress, 3);
                    el.innerText = Math.floor(ease * target).toLocaleString();
                    if (progress < 1) requestAnimationFrame(step);
                };
                requestAnimationFrame(step);
                obs.unobserve(el);
            });
        }, { threshold: 0.5 });
        numberEls.forEach(el => obs.observe(el));
    }

    /* ---- Boot ---- */
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.elementor-button').forEach(attachRipple);
        initNavScroll();
        initSparkles();
        animateCounters();
    });
}());