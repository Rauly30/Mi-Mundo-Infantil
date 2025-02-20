document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-links li');
    const mainContent = document.getElementById('mainContent');

    // Función para cargar el contenido de cada sección
    function loadSection(sectionId) {
        mainContent.innerHTML = ''; // Limpiar contenido anterior

        switch (sectionId) {
            case 'horario':
                mainContent.innerHTML = `
                    <h1>Horario de Clases</h1>
                    <div class="card">
                        <table>
                            <tr>
                                <th>Hora</th>
                                <th>Lunes</th>
                                <th>Martes</th>
                                <th>Miércoles</th>
                                <th>Jueves</th>
                                <th>Viernes</th>
                            </tr>
                            <tr>
                                <td>8:00 - 9:00</td>
                                <td>Matemáticas</td>
                                <td>Lenguaje</td>
                                <td>Ciencias</td>
                                <td>Arte</td>
                                <td>Educación Física</td>
                            </tr>
                            <tr>
                                <td>9:00 - 10:00</td>
                                <td>Lenguaje</td>
                                <td>Ciencias</td>
                                <td>Matemáticas</td>
                                <td>Música</td>
                                <td>Lenguaje</td>
                            </tr>
                            <tr>
                                <td>10:00 - 11:00</td>
                                <td>Recreo</td>
                                <td>Recreo</td>
                                <td>Recreo</td>
                                <td>Recreo</td>
                                <td>Recreo</td>
                            </tr>
                            <tr>
                                <td>11:00 - 12:00</td>
                                <td>Ciencias</td>
                                <td>Matemáticas</td>
                                <td>Lenguaje</td>
                                <td>Ciencias</td>
                                <td>Matemáticas</td>
                            </tr>
                        </table>
                    </div>
                `;
                break;
            case 'estudiantes':
                mainContent.innerHTML = `
                    <h1>Listado de Estudiantes</h1>
                    <div class="card">
                        <table>
                            <tr>
                                <th>Nombre</th>
                                <th>Asistencia</th>
                                <th>Calificación Promedio</th>
                                <th>Acciones</th>
                            </tr>
                            <tr>
                                <td>Ana García</td>
                                <td>95%</td>
                                <td>8.5</td>
                                <td><button class="btn" onclick="addComment('Ana García')">Añadir Comentario</button></td>
                            </tr>
                            <tr>
                                <td>Carlos Rodríguez</td>
                                <td>88%</td>
                                <td>7.9</td>
                                <td><button class="btn" onclick="addComment('Carlos Rodríguez')">Añadir Comentario</button></td>
                            </tr>
                            <tr>
                                <td>Laura Martínez</td>
                                <td>92%</td>
                                <td>9.2</td>
                                <td><button class="btn" onclick="addComment('Laura Martínez')">Añadir Comentario</button></td>
                            </tr>
                        </table>
                    </div>
                `;
                break;
            case 'comentarios':
                mainContent.innerHTML = `
                    <h1>Comentarios de Clase</h1>
                    <div class="card">
                        <form id="commentForm">
                            <div class="form-group">
                                <label for="studentName">Estudiante:</label>
                                <select id="studentName" required>
                                    <option value="">Seleccione un estudiante</option>
                                    <option value="Ana García">Ana García</option>
                                    <option value="Carlos Rodríguez">Carlos Rodríguez</option>
                                    <option value="Laura Martínez">Laura Martínez</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="commentText">Comentario:</label>
                                <textarea id="commentText" rows="4" required></textarea>
                            </div>
                            <button type="submit" class="btn">Agregar Comentario</button>
                        </form>
                    </div>
                    <div class="card">
                        <h2>Comentarios Recientes</h2>
                        <ul id="commentList">
                            <!-- Los comentarios se agregarán dinámicamente aquí -->
                        </ul>
                    </div>
                `;
                document.getElementById('commentForm').addEventListener('submit', addCommentFromForm);
                break;
            case 'evaluacion':
                mainContent.innerHTML = `
                    <h1>Plan de Evaluación</h1>
                    <div class="card">
                        <table>
                            <tr>
                                <th>Actividad</th>
                                <th>Fecha</th>
                                <th>Porcentaje</th>
                            </tr>
                            <tr>
                                <td>Examen Parcial</td>
                                <td>15/05/2025</td>
                                <td>30%</td>
                            </tr>
                            <tr>
                                <td>Proyecto Final</td>
                                <td>10/06/2025</td>
                                <td>40%</td>
                            </tr>
                            <tr>
                                <td>Participación en Clase</td>
                                <td>Continua</td>
                                <td>30%</td>
                            </tr>
                        </table>
                    </div>
                `;
                break;
        }
    }

    // Evento click para los enlaces de navegación
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            loadSection(link.getAttribute('data-section'));
        });
    });

    // Cargar la sección de horario por defecto
    loadSection('horario');
});

// Función para añadir comentarios desde el formulario
function addCommentFromForm(e) {
    e.preventDefault();
    const studentName = document.getElementById('studentName').value;
    const commentText = document.getElementById('commentText').value;
    const commentList = document.getElementById('commentList');
    const li = document.createElement('li');
    li.textContent = `${studentName}: ${commentText}`;
    commentList.appendChild(li);
    e.target.reset();
}

// Función para añadir comentarios desde la lista de estudiantes
function addComment(studentName) {
    const commentText = prompt(`Ingrese un comentario para ${studentName}:`);
    if (commentText) {
        const commentList = document.getElementById('commentList');
        const li = document.createElement('li');
        li.textContent = `${studentName}: ${commentText}`;
        commentList.appendChild(li);
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    // Configurar nombre de usuario
    document.getElementById('userName').textContent = "Profesor Ejemplo";

    // Cargar la primera sección por defecto
    loadSection('horario');
});