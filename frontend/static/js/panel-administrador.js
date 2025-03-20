document.addEventListener('DOMContentLoaded', () => {
    // Configuración inicial
    loadSection('estudiantes');
    setupNavigation();
    setupAlerts();
});

document.addEventListener('DOMContentLoaded', () => {
    const aulaSelect = document.getElementById('aula');
    const agregarBtn = document.querySelector('#agregarEstudianteModal .btn-primary');

    if (aulaSelect && agregarBtn) {
        aulaSelect.addEventListener('change', () => {
            const selectedOption = aulaSelect.options[aulaSelect.selectedIndex];
            const capacidad = parseInt(selectedOption.getAttribute('data-capacidad'));
            const estudiantes = parseInt(selectedOption.getAttribute('data-estudiantes'));

            if (estudiantes >= capacidad) {
                agregarBtn.disabled = true;
                alert(`El aula "${selectedOption.text}" ha alcanzado su capacidad máxima.`);
            } else {
                agregarBtn.disabled = false;
            }
        });
    }
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

// Función para mostrar/ocultar formularios
function toggleForm(formId) {
    const form = document.getElementById(formId);
    if (form.style.display === 'none' || form.style.display === '') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

// Configuración de alertas
function setupAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 3000);
    });
}