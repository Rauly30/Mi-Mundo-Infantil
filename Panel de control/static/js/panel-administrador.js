document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-links li');
    const mainContent = document.getElementById('mainContent');

    // Función para cargar el contenido de cada sección
    function loadSection(sectionId) {
        mainContent.innerHTML = ''; // Limpiar contenido anterior

        switch (sectionId) {
            case 'estudiantes':
                loadStudentsSection();
                break;
            case 'aulas':
                loadClassroomsSection();
                break;
            case 'profesores':
                loadTeachersSection();
                break;
            case 'accesos':
                mainContent.innerHTML = `
                    <h1>Control de Accesos</h1>
                    <div class="card">
                        <h2>Crear Nuevo Acceso</h2>
                        <form id="createAccessForm">
                            <div class="form-group">
                                <label for="userName">Nombre del Usuario:</label>
                                <input type="text" id="userName" required>
                            </div>
                            <div class="form-group">
                                <label for="userEmail">Correo Electrónico:</label>
                                <input type="email" id="userEmail" required>
                            </div>
                            <div class="form-group">
                                <label for="userRole">Rol:</label>
                                <select id="userRole" required>
                                    <option value="profesor">Profesor</option>
                                    <option value="administrador">Administrador</option>
                                    <option value="director">Director</option>
                                </select>
                            </div>
                            <button type="submit" class="btn">Crear Acceso</button>
                        </form>
                    </div>
                    <div class="card">
                        <h2>Accesos Actuales</h2>
                        <table>
                            <tr>
                                <th>Nombre</th>
                                <th>Correo Electrónico</th>
                                <th>Rol</th>
                                <th>Acciones</th>
                            </tr>
                            <tr>
                                <td>Juan Pérez</td>
                                <td>juan.perez@escuela.com</td>
                                <td>Profesor</td>
                                <td>
                                    <button class="btn" onclick="editAccess('Juan Pérez')">Editar</button>
                                    <button class="btn" onclick="deleteAccess('Juan Pérez')">Eliminar</button>
                                </td>
                            </tr>
                            <tr>
                                <td>María López</td>
                                <td>maria.lopez@escuela.com</td>
                                <td>Administrador</td>
                                <td>
                                    <button class="btn" onclick="editAccess('María López')">Editar</button>
                                    <button class="btn" onclick="deleteAccess('María López')">Eliminar</button>
                                </td>
                            </tr>
                        </table>
                    </div>
                `;
                document.getElementById('createAccessForm').addEventListener('submit', createAccess);
                break;
        }
    }

    function loadStudentsSection() {
        mainContent.innerHTML = `
            <h1>Gestión de Estudiantes</h1>
            <div class="card">
                <button class="btn" onclick="showAddStudentForm()">Agregar Estudiante</button>
                <div id="studentList" class="student-grid">
                    <!-- Los estudiantes se cargarán aquí dinámicamente -->
                </div>
            </div>
            <div id="addStudentForm" class="modal" style="display:none;">
                <div class="modal-content">
                    <h2>Agregar Nuevo Estudiante</h2>
                    <form id="newStudentForm">
                        <input type="text" id="studentName" placeholder="Nombre del estudiante" required>
                        <input type="number" id="studentAge" placeholder="Edad" required min="3" max="12">
                        <select id="studentLevel" required>
                            <option value="">Seleccione el nivel</option>
                            <option value="Preescolar">Preescolar</option>
                            <option value="Primaria">Primaria</option>
                        </select>
                        <button type="submit" class="btn">Guardar Estudiante</button>
                        <button type="button" class="btn" onclick="hideAddStudentForm()">Cancelar</button>
                    </form>
                </div>
            </div>
        `;
        loadStudents();
        document.getElementById('newStudentForm').addEventListener('submit', addStudent);
    }

    function loadClassroomsSection() {
        mainContent.innerHTML = `
            <h1>Asignación de Aulas</h1>
            <div class="classroom-container">
                <div class="classroom-section">
                    <h2>Preescolar</h2>
                    <div id="preschoolClassrooms" class="classroom-grid">
                        <!-- Las aulas de preescolar se cargarán aquí -->
                    </div>
                </div>
                <div class="classroom-section">
                    <h2>Primaria</h2>
                    <div id="primaryClassrooms" class="classroom-grid">
                        <!-- Las aulas de primaria se cargarán aquí -->
                    </div>
                </div>
            </div>
            <button class="btn" onclick="showAddClassroomForm()">Agregar Nueva Aula</button>
            <div id="addClassroomForm" class="modal" style="display:none;">
                <div class="modal-content">
                    <h2>Agregar Nueva Aula</h2>
                    <form id="newClassroomForm">
                        <input type="text" id="classroomName" placeholder="Nombre del aula" required>
                        <select id="classroomLevel" required>
                            <option value="">Seleccione el nivel</option>
                            <option value="Preescolar">Preescolar</option>
                            <option value="Primaria">Primaria</option>
                        </select>
                        <input type="number" id="classroomCapacity" placeholder="Capacidad" required min="1" max="30">
                        <button type="submit" class="btn">Guardar Aula</button>
                        <button type="button" class="btn" onclick="hideAddClassroomForm()">Cancelar</button>
                    </form>
                </div>
            </div>
        `;
        loadClassrooms();
        document.getElementById('newClassroomForm').addEventListener('submit', addClassroom);
    }

    function loadTeachersSection() {
        mainContent.innerHTML = `
            <h1>Gestión de Profesores</h1>
            <div class="card">
                <button class="btn" onclick="showAddTeacherForm()">Agregar Profesor</button>
                <div id="teacherList" class="teacher-grid">
                    <!-- Los profesores se cargarán aquí dinámicamente -->
                </div>
            </div>
            <div id="addTeacherForm" class="modal" style="display:none;">
                <div class="modal-content">
                    <h2>Agregar Nuevo Profesor</h2>
                    <form id="newTeacherForm">
                        <input type="text" id="teacherName" placeholder="Nombre del profesor" required>
                        <select id="teacherSpecialty" required>
                            <option value="">Seleccione la especialidad</option>
                            <option value="Educación Infantil">Educación Infantil</option>
                            <option value="Educación Primaria">Educación Primaria</option>
                        </select>
                        <button type="submit" class="btn">Guardar Profesor</button>
                        <button type="button" class="btn" onclick="hideAddTeacherForm()">Cancelar</button>
                    </form>
                </div>
            </div>
        `;
        loadTeachers();
        document.getElementById('newTeacherForm').addEventListener('submit', addTeacher);
    }

    function loadAccessSection() {
        // El contenido de esta sección se mantiene igual que antes
    }

    // Evento click para los enlaces de navegación
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            loadSection(link.getAttribute('data-section'));
        });
    });

    // Cargar la sección de estudiantes por defecto
    loadSection('estudiantes');
});

// Funciones para cargar datos
function loadStudents() {
    // Simulación de carga de estudiantes
    const students = [
        { id: 1, name: "Carlos Rodríguez", age: 5, level: "Preescolar", classroom: "Sala Amarilla" },
        { id: 2, name: "Ana García", age: 7, level: "Primaria", classroom: "2° Grado A" },
        // Añadir más estudiantes aquí
    ];

    const studentList = document.getElementById('studentList');
    studentList.innerHTML = students.map(student => `
        <div class="student-card ${student.level.toLowerCase()}">
            <h3>${student.name}</h3>
            <p>Edad: ${student.age}</p>
            <p>Nivel: ${student.level}</p>
            <p>Aula: ${student.classroom}</p>
            <button class="btn" onclick="editStudent(${student.id})">Editar</button>
            <button class="btn" onclick="deleteStudent(${student.id})">Eliminar</button>
        </div>
    `).join('');
}

function loadClassrooms() {
    // Simulación de carga de aulas
    const classrooms = [
        { id: 1, name: "Sala Amarilla", level: "Preescolar", capacity: 20, students: 15 },
        { id: 2, name: "2° Grado A", level: "Primaria", capacity: 25, students: 22 },
        // Añadir más aulas aquí
    ];

    const preschoolClassrooms = document.getElementById('preschoolClassrooms');
    const primaryClassrooms = document.getElementById('primaryClassrooms');

    classrooms.forEach(classroom => {
        const classroomElement = `
            <div class="classroom-card">
                <h3>${classroom.name}</h3>
                <p>Capacidad: ${classroom.students}/${classroom.capacity}</p>
                <div class="progress-bar">
                    <div class="progress" style="width: ${(classroom.students / classroom.capacity) * 100}%"></div>
                </div>
                <button class="btn" onclick="viewClassroom(${classroom.id})">Ver Detalles</button>
            </div>
        `;

        if (classroom.level === "Preescolar") {
            preschoolClassrooms.innerHTML += classroomElement;
        } else {
            primaryClassrooms.innerHTML += classroomElement;
        }
    });
}

function loadTeachers() {
    // Simulación de carga de profesores
    const teachers = [
        { id: 1, name: "Juan Pérez", specialty: "Educación Infantil", classroom: "Sala Amarilla" },
        { id: 2, name: "María López", specialty: "Educación Primaria", classroom: "2° Grado A" },
        // Añadir más profesores aquí
    ];

    const teacherList = document.getElementById('teacherList');
    teacherList.innerHTML = teachers.map(teacher => `
        <div class="teacher-card">
            <h3>${teacher.name}</h3>
            <p>Especialidad: ${teacher.specialty}</p>
            <p>Aula Asignada: ${teacher.classroom}</p>
            <button class="btn" onclick="editTeacher(${teacher.id})">Editar</button>
            <button class="btn" onclick="deleteTeacher(${teacher.id})">Eliminar</button>
        </div>
    `).join('');
}

// Funciones para manejar acciones específicas
function showAddStudentForm() {
    document.getElementById('addStudentForm').style.display = 'block';
}

function hideAddStudentForm() {
    document.getElementById('addStudentForm').style.display = 'none';
}

function addStudent(e) {
    e.preventDefault();
    const name = document.getElementById('studentName').value;
    const age = document.getElementById('studentAge').value;
    const level = document.getElementById('studentLevel').value;
    alert(`Agregando nuevo estudiante: ${name}, Edad: ${age}, Nivel: ${level}`);
    // Aquí iría la lógica para guardar el nuevo estudiante en la base de datos
    hideAddStudentForm();
    loadStudents(); // Recargar la lista de estudiantes
}

function editStudent(studentId) {
    alert(`Editando información del estudiante con ID: ${studentId}`);
    // Aquí iría la lógica para abrir un formulario de edición de estudiante
}

function deleteStudent(studentId) {
    if (confirm(`¿Está seguro de que desea eliminar al estudiante con ID: ${studentId}?`)) {
        alert(`Estudiante con ID: ${studentId} eliminado`);
        // Aquí iría la lógica para eliminar al estudiante de la base de datos
        loadStudents(); // Recargar la lista de estudiantes
    }
}

function showAddClassroomForm() {
    document.getElementById('addClassroomForm').style.display = 'block';
}

function hideAddClassroomForm() {
    document.getElementById('addClassroomForm').style.display = 'none';
}

function addClassroom(e) {
    e.preventDefault();
    const name = document.getElementById('classroomName').value;
    const level = document.getElementById('classroomLevel').value;
    const capacity = document.getElementById('classroomCapacity').value;
    alert(`Agregando nueva aula: ${name}, Nivel: ${level}, Capacidad: ${capacity}`);
    // Aquí iría la lógica para guardar la nueva aula en la base de datos
    hideAddClassroomForm();
    loadClassrooms(); // Recargar la lista de aulas
}

function viewClassroom(classroomId) {
    alert(`Mostrando detalles del aula con ID: ${classroomId}`);
    // Aquí iría la lógica para mostrar una vista detallada del aula y sus estudiantes
}

function showAddTeacherForm() {
    document.getElementById('addTeacherForm').style.display = 'block';
}

function hideAddTeacherForm() {
    document.getElementById('addTeacherForm').style.display = 'none';
}

function addTeacher(e) {
    e.preventDefault();
    const name = document.getElementById('teacherName').value;
    const specialty = document.getElementById('teacherSpecialty').value;
    alert(`Agregando nuevo profesor: ${name}, Especialidad: ${specialty}`);
    // Aquí iría la lógica para guardar el nuevo profesor en la base de datos
    hideAddTeacherForm();
    loadTeachers(); // Recargar la lista de profesores
}

function editTeacher(teacherId) {
    alert(`Editando información del profesor con ID: ${teacherId}`);
    // Aquí iría la lógica para abrir un formulario de edición de profesor
}

function deleteTeacher(teacherId) {
    if (confirm(`¿Está seguro de que desea eliminar al profesor con ID: ${teacherId}?`)) {
        alert(`Profesor con ID: ${teacherId} eliminado`);
        // Aquí iría la lógica para eliminar al profesor de la base de datos
        loadTeachers(); // Recargar la lista de profesores
    }
}

function createAccess(e) {
    e.preventDefault();
    const name = document.getElementById('userName').value;
    const email = document.getElementById('userEmail').value;
    const role = document.getElementById('userRole').value;
    alert(`Creando acceso para ${name} (${email}) con rol de ${role}`);
    // Aquí iría la lógica para guardar el nuevo acceso en la base de datos
}

function editAccess(userName) {
    alert(`Editando acceso de ${userName}`);
    // Aquí iría la lógica para abrir un formulario de edición de acceso
}

function deleteAccess(userName) {
    if (confirm(`¿Está seguro de que desea eliminar el acceso de "${userName}"?`)) {
        alert(`Acceso de "${userName}" eliminado`);
        // Aquí iría la lógica para eliminar el acceso de la base de datos
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    // Configurar nombre de usuario
    document.getElementById('userName').textContent = "Administrador Ejemplo";
});