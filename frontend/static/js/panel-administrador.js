document.addEventListener('DOMContentLoaded', () => {
    // Configuración inicial
    loadSection('estudiantes');
    setupNavigation();
    
    // Configurar formularios
    document.getElementById('studentForm').addEventListener('submit', handleStudentSubmit);
    
    document.getElementById('showAddStudentFormButton').addEventListener('click', showAddStudentForm);
});

// Configuración de la navegación
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-links li');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            loadSection(link.dataset.section);
        });
    });
}

// Función para cargar secciones
function loadSection(sectionName) {
    switch(sectionName) {
        case 'estudiantes':
            loadEstudiantes();
            break;
        case 'aulas':
            loadAulas();
            break;
        case 'profesores':
            loadProfesores();
            break;
        case 'accesos':
            loadAccesos();
            break;
    }
}

// Token CSRF
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

// Función para cargar estudiantes
async function loadEstudiantes() {
    try {
        const response = await fetch('/api/estudiantes/');
        const estudiantes = await response.json();
        
        const studentList = document.getElementById('studentList');
        studentList.innerHTML = estudiantes.map(estudiante => `
            <div class="student-card">
                <h3>${estudiante.nombre}</h3>
                <p>Edad: ${estudiante.edad} años</p>
                <p>Nivel: ${estudiante.nivel}</p>
                <p>Aula: ${estudiante.aula || 'No asignada'}</p>
                <div class="card-actions">
                    <button onclick="editStudent(${estudiante.id})" class="btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button onclick="deleteStudent(${estudiante.id})" class="btn-delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar estudiantes:', error);
        showError('Error al cargar los estudiantes');
    }
}

// Función para mostrar formulario de estudiante
function showAddStudentForm() {
    document.getElementById('modalTitle').textContent = 'Agregar Estudiante';
    document.getElementById('studentId').value = '';
    document.getElementById('studentForm').reset();
    document.getElementById('studentModal').style.display = 'block';
    loadAulasForSelect();
}

// Cargar aulas en el formulario
async function loadAulasForSelect() {
    try {
        const response = await fetch('/api/aulas/');
        const aulas = await response.json();

        const aulaSelect = document.getElementById('aula');
        aulaSelect.innerHTML = aulas.map(aula => `
            <option value="${aula.id}">${aula.nombre} (${aula.nivel})</option>
        `).join('');
    } catch (error) {
        console.error('Error al cargar aulas:', error);
        showError('Error al cargar las aulas disponibles');
    }
}

// Manejo del formulario de estudiante
async function handleStudentSubmit(e) {
    e.preventDefault();
    
    const studentId = document.getElementById('studentId').value;
    const formData = {
        nombre: document.getElementById('nombre').value,
        edad: document.getElementById('edad').value,
        nivel: document.getElementById('nivel').value,
        aula: document.getElementById('aula').value
    };
    
    const url = studentId ? `/api/estudiantes/${studentId}/` : '/api/estudiantes/';
    
    try {
        const response = await fetch(url, {
            method: studentId ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            closeModal();
            loadEstudiantes();
            showSuccess(studentId ? 'Estudiante actualizado' : 'Estudiante creado');
        } else {
            throw new Error('Error en la operación');
        }
    } catch (error) {
        console.error('Error al guardar el estudiante:', error);
        showError('Error al guardar el estudiante');
    }
}

// Eliminar estudiante
async function deleteStudent(id) {
    if (confirm('¿Está seguro de eliminar este estudiante?')) {
        try {
            const response = await fetch(`/api/estudiantes/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            if (response.ok) {
                loadEstudiantes();
                showSuccess('Estudiante eliminado');
            } else {
                throw new Error('Error en la eliminación');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Error al eliminar el estudiante');
        }
    }
}

// Funciones auxiliares
function closeModal() {
    document.getElementById('studentModal').style.display = 'none';
}

function showSuccess(message) {
    alert(message);
}

function showError(message) {
    alert(message);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            if (cookie.trim().startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.trim().substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}
