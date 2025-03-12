document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav-links .nav-item a");
    const sections = document.querySelectorAll("#mainContent > div");

    navLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetSection = this.closest('.nav-item').getAttribute("data-section");

            sections.forEach((section) => {
                if (section.id === targetSection) {
                    section.style.display = "block";
                } else {
                    section.style.display = "none";
                }
            });
        });
    });

    // Mostrar la primera sección por defecto
    if (sections.length > 0) {
        sections[0].style.display = "block";
    }

    // Manejar el formulario de comentarios de clase
    const commentFormClase = document.getElementById('commentFormClase');
    if (commentFormClase) {
        commentFormClase.addEventListener('submit', (e) => {
            e.preventDefault();
            const evaluationId = document.getElementById('evaluationId').value;
            const commentText = document.getElementById('commentTextClase').value;

            fetch('/panel/profesor/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    'action': 'agregar_comentario',
                    'evaluacion_id': evaluationId,
                    'texto': commentText
                })
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload(); // Recarga la página para mostrar el nuevo comentario
                } else {
                    alert('Error al agregar el comentario');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    // Manejar el formulario de edición de comentarios
    document.querySelectorAll('.edit-comment-form').forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            fetch('/panel/profesor/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams(formData)
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload(); // Recarga la página para mostrar el comentario editado
                } else {
                    alert('Error al editar el comentario');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // Manejar el formulario de eliminación de comentarios
    document.querySelectorAll('.delete-comment-form').forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (confirm('¿Estás seguro de que deseas eliminar este comentario?')) {
                const formData = new FormData(form);
                fetch('/panel/profesor/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: new URLSearchParams(formData)
                })
                .then(response => {
                    if (response.ok) {
                        window.location.reload(); // Recarga la página para mostrar el comentario eliminado
                    } else {
                        alert('Error al eliminar el comentario');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    });
});