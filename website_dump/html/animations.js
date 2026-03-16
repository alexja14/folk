document.addEventListener("DOMContentLoaded", () => {
    // 1. Setup Scroll Reveal Setup
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Run once
            }
        });
    }, observerOptions);

    // Find elements to reveal: headings, text editors, inner images
    const elementsToReveal = document.querySelectorAll(
        '.elementor-widget-heading, .elementor-widget-text-editor, .elementor-widget-image, .uc-before-after'
    );
    
    elementsToReveal.forEach((el, index) => {
        el.classList.add('bellissimo-reveal');
        // Stagger delay based on index slightly so they don't all pop at once
        el.style.transitionDelay = `${(index % 4) * 0.1}s`;
        observer.observe(el);
    });

    // 2. Setup Cards (Interactive Hover)
    // We target common Elementor card-like structures
    const cards = document.querySelectorAll(
        '.e-con-boxed > .e-con-inner > .e-child, .elementor-column-wrap > .elementor-widget-wrap, .elementor-cta'
    );
    cards.forEach(card => {
        card.classList.add('bellissimo-card');
    });
});