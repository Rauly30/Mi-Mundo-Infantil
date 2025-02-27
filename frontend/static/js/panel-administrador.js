document.addEventListener('DOMContentLoaded', () => {
    // Configuración inicial
    loadSection('estudiantes');
    setupNavigation();
});

// Configuración de la navegación
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-links .nav-item');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault(); // Evita el comportamiento predeterminado del enlace
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            const sectionName = link.getAttribute('data-section');
            loadSection(sectionName);
        });
    });
}

// Función para cargar secciones
function loadSection(sectionName) {
    const sections = document.querySelectorAll('#mainContent > div');
    sections.forEach(section => {
        section.style.display = 'none'; // Oculta todas las secciones
    });

    // Muestra la sección seleccionada
    const activeSection = document.getElementById(sectionName);
    if (activeSection) {
        activeSection.style.display = 'block';
    }
}