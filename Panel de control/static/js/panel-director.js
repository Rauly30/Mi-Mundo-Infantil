document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-links li');
    const mainContent = document.getElementById('mainContent');

    // Función para cargar el contenido de cada sección
    function loadSection(sectionId) {
        mainContent.innerHTML = ''; // Limpiar contenido anterior

        switch (sectionId) {
            case 'clases':
                mainContent.innerHTML = `
                    <h1>Listado de Clases</h1>
                    <div class="card">
                        <table>
                            <tr>
                                <th>Grado</th>
                                <th>Profesor</th>
                                <th>Número de Estudiantes</th>
                                <th>Acciones</th>
                            </tr>
                            <tr>
                                <td>3° A</td>
                                <td>María López</td>
                                <td>25</td>
                                <td><button class="btn" onclick="viewClassDetails('3° A')">Ver Detalles</button></td>
                            </tr>
                            <tr>
                                <td>4° B</td>
                                <td>Juan Pérez</td>
                                <td>22</td>
                                <td><button class="btn" onclick="viewClassDetails('4° B')">Ver Detalles</button></td>
                            </tr>
                            <tr>
                                <td>5° C</td>
                                <td>Ana Rodríguez</td>
                                <td>20</td>
                                <td><button class="btn" onclick="viewClassDetails('5° C')">Ver Detalles</button></td>
                            </tr>
                        </table>
                    </div>
                `;
                break;
            case 'evaluaciones':
                mainContent.innerHTML = `
                    <h1>Evaluaciones</h1>
                    <div class="card">
                        <h2>Planes de Evaluación por Clase</h2>
                        <table>
                            <tr>
                                <th>Clase</th>
                                <th>Profesor</th>
                                <th>Acciones</th>
                            </tr>
                            <tr>
                                <td>3° A</td>
                                <td>María López</td>
                                <td>
                                    <button class="btn" onclick="viewEvaluationPlan('3° A')">Ver Plan</button>
                                    <button class="btn" onclick="addCommentToEvaluation('3° A')">Añadir Comentario</button>
                                </td>
                            </tr>
                            <tr>
                                <td>4° B</td>
                                <td>Juan Pérez</td>
                                <td>
                                    <button class="btn" onclick="viewEvaluationPlan('4° B')">Ver Plan</button>
                                    <button class="btn" onclick="addCommentToEvaluation('4° B')">Añadir Comentario</button>
                                </td>
                            </tr>
                            <tr>
                                <td>5° C</td>
                                <td>Ana Rodríguez</td>
                                <td>
                                    <button class="btn" onclick="viewEvaluationPlan('5° C')">Ver Plan</button>
                                    <button class="btn" onclick="addCommentToEvaluation('5° C')">Añadir Comentario</button>
                                </td>
                            </tr>
                        </table>
                    </div>
                `;
                break;
            case 'eventos':
                mainContent.innerHTML = `
                    <h1>Eventos y Días Especiales</h1>
                    <div class="card">
                        <button class="btn" onclick="addEvent()">Agregar Evento</button>
                        <table>
                            <tr>
                                <th>Fecha</th>
                                <th>Evento</th>
                                <th>Descripción</th>
                                <th>Acciones</th>
                            </tr>
                            <tr>
                                <td>01/06/2025</td>
                                <td>Día del Niño</td>
                                <td>Celebración especial para todos los estudiantes</td>
                                <td>
                                    <button class="btn" onclick="editEvent('Día del Niño')">Editar</button>
                                    <button class="btn" onclick="deleteEvent('Día del Niño')">Eliminar</button>
                                </td>
                            </tr>
                            <tr>
                                <td>15/09/2025</td>
                                <td>Feria de Ciencias</td>
                                <td>Exhibición de proyectos científicos de los estudiantes</td>
                                <td>
                                    <button class="btn" onclick="editEvent('Feria de Ciencias')">Editar</button>
                                    <button class="btn" onclick="deleteEvent('Feria de Ciencias')">Eliminar</button>
                                </td>
                            </tr>
                        </table>
                    </div>
                `;
                break;
            case 'profesores':
                mainContent.innerHTML = `
                    <h1>Listado de Profesores</h1>
                    <div class="card">
                        <table>
                            <tr>
                                <th>Nombre</th>
                                <th>Especialidad</th>
                                <th>Clases Asignadas</th>
                                <th>Acciones</th>
                            </tr>
                            <tr>
                                <td>María López</td>
                                <td>Matemáticas</td>
                                <td>3° A, 4° B</td>
                                <td>
                                    <button class="btn" onclick="viewTeacherDetails('María López')">Ver Detalles</button>
                                    <button class="btn" onclick="addCommentToTeacher('María López')">Añadir Comentario</button>
                                </td>
                            </tr>
                            <tr>
                                <td>Juan Pérez</td>
                                <td>Lenguaje</td>
                                <td>4° B, 5° C</td>
                                <td>
                                    <button class="btn" onclick="viewTeacherDetails('Juan Pérez')">Ver Detalles</button>
                                    <button class="btn" onclick="addCommentToTeacher('Juan Pérez')">Añadir Comentario</button>
                                </td>
                            </tr>
                            <tr>
                                <td>Ana Rodríguez</td>
                                <td>Ciencias</td>
                                <td>5° C, 6° A</td>
                                <td>
                                    <button class="btn" onclick="viewTeacherDetails('Ana Rodríguez')">Ver Detalles</button>
                                    <button class="btn" onclick="addCommentToTeacher('Ana Rodríguez')">Añadir Comentario</button>
                                </td>
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

    // Cargar la sección de clases por defecto
    loadSection('clases');
});

// Funciones para manejar acciones específicas
function viewClassDetails(className) {
    alert(`Viendo detalles de la clase ${className}`);
}

function viewEvaluationPlan(className) {
    alert(`Viendo plan de evaluación de la clase ${className}`);
}

function addCommentToEvaluation(className) {
    const comment = prompt(`Añadir comentario al plan de evaluación de la clase ${className}:`);
    if (comment) {
        alert(`Comentario añadido al plan de evaluación de ${className}: ${comment}`);
    }
}

function addEvent() {
    alert('Agregando nuevo evento');
    // Aquí iría la lógica para abrir un formulario de nuevo evento
}

function editEvent(eventName) {
    alert(`Editando evento: ${eventName}`);
    // Aquí iría la lógica para abrir un formulario de edición de evento
}

function deleteEvent(eventName) {
    if (confirm(`¿Está seguro de que desea eliminar el evento "${eventName}"?`)) {
        alert(`Evento "${eventName}" eliminado`);
        // Aquí iría la lógica para eliminar el evento de la base de datos
    }
}

function viewTeacherDetails(teacherName) {
    alert(`Viendo detalles del profesor ${teacherName}`);
    // Aquí iría la lógica para mostrar una ventana modal o navegar a una página de detalles del profesor
}

function addCommentToTeacher(teacherName) {
    const comment = prompt(`Añadir comentario para el profesor ${teacherName}:`);
    if (comment) {
        alert(`Comentario añadido para ${teacherName}: ${comment}`);
        // Aquí iría la lógica para guardar el comentario en la base de datos
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    // Configurar nombre de usuario
    document.getElementById('userName').textContent = "Director Ejemplo";
});