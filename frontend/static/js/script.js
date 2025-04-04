// Initialize AOS (Animate On Scroll)
AOS.init({
    duration: 1000,
    once: true
});

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    menuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        menuToggle.classList.toggle('active');
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('active');
        });
    });
});

// Smooth Scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        const headerOffset = 70;
        const elementPosition = target.offsetTop;
        const offsetPosition = elementPosition - headerOffset;

        window.scrollTo({
            top: offsetPosition,
            behavior: "smooth"
        });
    });
});

// Navbar Background Change on Scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = '#ffffff';
        navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    } else {
        navbar.style.background = '#ffffff';
        navbar.style.boxShadow = 'none';
    }
});

// Image Gallery
document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', function() {
        this.classList.toggle('expanded');
    });
});

// Image Gallery
document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', function() {
        this.classList.toggle('expanded');
    });
});

// Floating Animation for Hero Image
function floatAnimation() {
    const heroImage = document.querySelector('.hero-image img');
    if (heroImage) {
        let float = true;
        setInterval(() => {
            if (float) {
                heroImage.style.transform = 'translateY(-20px)';
            } else {
                heroImage.style.transform = 'translateY(0)';
            }
            float = !float;
        }, 3000);
    }
}

// Initialize floating animation
document.addEventListener('DOMContentLoaded', floatAnimation);

// Intersection Observer for Animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('slide-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});
