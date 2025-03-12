document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".show-students-btn").forEach(button => {
        button.addEventListener("click", function () {
            const aulaId = this.dataset.aulaId;
            fetch(`/api/aulas/${aulaId}/estudiantes/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    const modalBody = document.querySelector("#studentsModal .modal-body tbody");
                    modalBody.innerHTML = data.map(student => `
                        <tr>
                            <td>${student.nombre}</td>
                            <td>${student.edad} años</td>
                        </tr>
                    `).join("");
                    const studentsModal = new bootstrap.Modal(document.getElementById('studentsModal'));
                    studentsModal.show();
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        });
    });

    // Add event listeners for navigation links
    document.querySelectorAll(".nav-links .nav-item a").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetSection = this.getAttribute("href").substring(1);
            document.querySelectorAll("#mainContent > div").forEach(section => {
                section.style.display = section.id === targetSection ? "block" : "none";
            });
        });
    });

    // Mostrar la primera sección por defecto
    const sections = document.querySelectorAll("#mainContent > div");
    if (sections.length > 0) {
        sections[0].style.display = "block";
    }
});
document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.nav-links .nav-item a');
    const sections = document.querySelectorAll('#mainContent > div');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // Ocultar todas las secciones
            sections.forEach(section => {
                section.style.display = 'none';
            });

            // Mostrar la sección correspondiente al enlace clickeado
            const targetSection = document.querySelector(this.getAttribute('href'));
            if (targetSection) {
                targetSection.style.display = 'block';
            }
        });
    });
});