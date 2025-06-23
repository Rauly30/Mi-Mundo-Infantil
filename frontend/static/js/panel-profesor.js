document.addEventListener("DOMContentLoaded", () => {
  // Estado de la aplicación
  const state = {
    currentSection: "dashboard",
    searchTimeout: null,
    activeModal: null,
  }

  // Cacheo de elementos del DOM
  const DOM = {
    navLinks: document.querySelectorAll(".nav-links .nav-item"),
    sections: document.querySelectorAll(".content-section"),
    sectionTitle: document.getElementById("sectionTitle"),
    currentSectionBreadcrumb: document.getElementById("currentSection"),
    refreshBtn: document.getElementById("refreshBtn"),
  }

  // Configuración de secciones
  const sectionsConfig = {
    dashboard: { title: "Dashboard del Profesor", icon: "fas fa-tachometer-alt" },
    estudiantes: { title: "Mis Estudiantes", icon: "fas fa-child" },
    boletines: { title: "Gestión de Boletines", icon: "fas fa-file-alt" },
    comentarios: { title: "Gestión de Comentarios", icon: "fas fa-comments" },
    evaluaciones: { title: "Evaluaciones", icon: "fas fa-clipboard-check" },
    eventos: { title: "Eventos", icon: "fas fa-calendar-day" },
  }

  // Inicialización
  function init() {
    setupNavigation()
    setupModals()
    setupFormValidation()
    setupEventListeners()
    showSection(state.currentSection)
    loadInitialData()

    console.log("Panel del profesor inicializado correctamente")
  }

  // NAVEGACIÓN --------------------------------------------------------
  function setupNavigation() {
    DOM.navLinks.forEach((link) => {
      link.addEventListener("click", function (e) {
        e.preventDefault()
        const targetSection = this.dataset.section
        if (targetSection && targetSection !== state.currentSection) {
          showSection(targetSection)
          setActiveNavItem(this)
        }
      })
    })
  }

  function showSection(sectionName) {
    if (!sectionsConfig[sectionName]) {
      console.error(`Sección ${sectionName} no configurada`)
      return
    }

    // Ocultar todas las secciones
    DOM.sections.forEach((section) => {
      section.style.display = "none"
    })

    // Mostrar sección seleccionada
    const targetSection = document.getElementById(sectionName)
    if (targetSection) {
      targetSection.style.display = "block"
      state.currentSection = sectionName

      updateSectionHeader(sectionName)
      loadSectionData(sectionName)

      // Actualizar navegación activa
      DOM.navLinks.forEach((item) => {
        item.classList.remove("active")
        if (item.dataset.section === sectionName) {
          item.classList.add("active")
        }
      })
    }
  }

  function updateSectionHeader(sectionName) {
    const config = sectionsConfig[sectionName]
    DOM.sectionTitle.textContent = config.title
    DOM.currentSectionBreadcrumb.textContent = config.title
  }

  function setActiveNavItem(activeItem) {
    DOM.navLinks.forEach((item) => {
      item.classList.remove("active")
    })
    activeItem.classList.add("active")
  }

  // MODALES Y FORMULARIOS ---------------------------------------------
  function setupModals() {
    // Inicializar modales de Bootstrap
    document.querySelectorAll('[data-bs-toggle="modal"]').forEach((trigger) => {
      trigger.addEventListener("click", function () {
        const target = this.dataset.bsTarget
        if (target) {
          const modalElement = document.querySelector(target)
          if (modalElement) {
            state.activeModal = new window.bootstrap.Modal(modalElement)
          }
        }
      })
    })
  }

  function setupFormValidation() {
    // Validación de formularios Bootstrap
    document.querySelectorAll(".needs-validation").forEach((form) => {
      form.addEventListener(
        "submit",
        (e) => {
          if (!form.checkValidity()) {
            e.preventDefault()
            e.stopPropagation()
            showNotification("Por favor complete todos los campos requeridos", "warning")
          }
          form.classList.add("was-validated")
        },
        false,
      )
    })

    // Validaciones específicas
    setupSpecificValidations()
  }

  function setupSpecificValidations() {
    // Validación de calificación
    document.querySelectorAll('input[name="calificacion"]').forEach((input) => {
      input.addEventListener("input", function () {
        const value = Number.parseFloat(this.value)
        if (isNaN(value) || value < 0 || value > 20) {
          this.setCustomValidity("La calificación debe estar entre 0 y 20")
        } else {
          this.setCustomValidity("")
        }
      })
    })

    // Validación de texto de comentarios
    document.querySelectorAll('textarea[name="texto"]').forEach((textarea) => {
      textarea.addEventListener("input", function () {
        const value = this.value.trim()
        if (value.length < 10) {
          this.setCustomValidity("El comentario debe tener al menos 10 caracteres")
        } else if (value.length > 500) {
          this.setCustomValidity("El comentario no puede exceder 500 caracteres")
        } else {
          this.setCustomValidity("")
        }
      })
    })
  }

  function setupEventListeners() {
    // Botón de refrescar
    if (DOM.refreshBtn) {
      DOM.refreshBtn.addEventListener("click", function () {
        this.classList.add("fa-spin")
        setTimeout(() => {
          this.classList.remove("fa-spin")
          showNotification("Datos actualizados", "success")
          loadSectionData(state.currentSection)
        }, 1000)
      })
    }

    // Acciones rápidas del dashboard
    document.querySelectorAll(".quick-action-card").forEach((card) => {
      card.addEventListener("click", function () {
        if (!this.dataset.bsTarget && !this.onclick) {
          this.style.transform = "scale(0.95)"
          setTimeout(() => {
            this.style.transform = ""
          }, 150)
        }
      })
    })
  }

  // DATOS Y CARGA -----------------------------------------------------
  function loadInitialData() {
    updateDashboardStats()
    loadRecentComments()
    loadUpcomingEvents()
  }

  function updateDashboardStats() {
    animateElements(".performance-metric", 100)
    animateElements(".quick-action-card", 150)
  }

  function loadRecentComments() {
    animateElements(".comment-card", 200)
  }

  function loadUpcomingEvents() {
    animateElements(".event-item", 200)
  }

  function loadSectionData(sectionName) {
    switch (sectionName) {
      case "estudiantes":
        animateElements(".estudiante-card", 100)
        break
      case "boletines":
        animateElements("tbody tr", 50)
        break
      case "comentarios":
        animateElements(".comment-card", 100)
        break
      case "evaluaciones":
        animateElements("tbody tr", 50)
        break
      case "eventos":
        animateElements(".event-card", 100)
        break
    }
  }

  function animateElements(selector, delay, startIndex = 0) {
    document.querySelectorAll(selector).forEach((el, index) => {
      setTimeout(
        () => {
          el.classList.add("animate-fade-in")
        },
        (startIndex + index) * delay,
      )
    })
  }

  // UTILIDADES --------------------------------------------------------
  function showNotification(message, type = "info") {
    const notification = document.createElement("div")
    notification.className = `alert alert-${type} notification-toast`
    notification.innerHTML = `
            <i class="fas fa-${getIconForType(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `

    notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            animation: slideInRight 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `

    document.body.appendChild(notification)

    setTimeout(() => {
      if (notification.parentNode) {
        notification.style.animation = "slideOutRight 0.3s ease"
        setTimeout(() => notification.remove(), 300)
      }
    }, 4000)
  }

  function getIconForType(type) {
    const icons = {
      success: "check-circle",
      danger: "exclamation-triangle",
      warning: "exclamation-circle",
      info: "info-circle",
    }
    return icons[type] || "info-circle"
  }

  // FUNCIONES GLOBALES ------------------------------------------------
  window.crearBoletin = (estudianteId) => {
    const modal = new window.bootstrap.Modal(document.getElementById("agregarBoletinModal"))
    const selectEstudiante = document.getElementById("estudianteBoletin")

    if (selectEstudiante) {
      selectEstudiante.value = estudianteId
    }

    modal.show()
  }

  window.confirmarEliminacion = (tipo, id) => {
    const tipoTexto = {
      boletin: "boletín",
      comentario: "comentario",
      evaluacion: "evaluación",
    }

    if (
      confirm(`¿Estás seguro de que deseas eliminar este ${tipoTexto[tipo] || tipo}? Esta acción no se puede deshacer.`)
    ) {
      const form = document.createElement("form")
      form.method = "POST"
      form.action = window.location.href

      // CSRF Token
      const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")
      if (csrfToken) {
        const csrfInput = document.createElement("input")
        csrfInput.type = "hidden"
        csrfInput.name = "csrfmiddlewaretoken"
        csrfInput.value = csrfToken.value
        form.appendChild(csrfInput)
      }

      // Acción e ID
      const actionInput = document.createElement("input")
      actionInput.type = "hidden"
      actionInput.name = "action"
      actionInput.value = `eliminar_${tipo}`
      form.appendChild(actionInput)

      const idInput = document.createElement("input")
      idInput.type = "hidden"
      idInput.name = "id"
      idInput.value = id
      form.appendChild(idInput)

      document.body.appendChild(form)
      form.submit()
    }
  }

  window.verDetallesBoletin = (boletinId) => {
    // Implementar lógica para mostrar detalles del boletín
    showNotification("Función en desarrollo", "info")
  }

  window.editarBoletin = (boletinId) => {
    // Implementar lógica para editar boletín
    showNotification("Función en desarrollo", "info")
  }

  window.editarComentario = (comentarioId) => {
    // Implementar lógica para editar comentario
    showNotification("Función en desarrollo", "info")
  }

  // Exponer función showSection globalmente
  window.showSection = showSection

  // Funciones de utilidad para calificaciones
  window.getGradeClass = (calificacion) => {
    if (calificacion >= 18) return "grade-excellent"
    if (calificacion >= 14) return "grade-good"
    if (calificacion >= 10) return "grade-regular"
    return "grade-poor"
  }

  window.getGradeText = (calificacion) => {
    if (calificacion >= 18) return "Excelente"
    if (calificacion >= 14) return "Bueno"
    if (calificacion >= 10) return "Regular"
    return "Deficiente"
  }

  // Función para generar reportes
  window.generarReporte = (tipo) => {
    showNotification(`Generando reporte de ${tipo}...`, "info")

    // Simular generación de reporte
    setTimeout(() => {
      showNotification(`Reporte de ${tipo} generado exitosamente`, "success")
    }, 2000)
  }

  // Función para exportar datos
  window.exportarDatos = (formato) => {
    showNotification(`Exportando datos en formato ${formato}...`, "info")

    // Simular exportación
    setTimeout(() => {
      showNotification(`Datos exportados exitosamente en ${formato}`, "success")
    }, 1500)
  }

  // Iniciar la aplicación
  init()

  // Agregar estilos de animación
  const style = document.createElement("style")
  style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.5s ease forwards;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .notification-toast {
            border-left: 4px solid;
        }
        
        .quick-action-card {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .quick-action-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .quick-action-card:active {
            transform: scale(0.95);
        }
        
        .performance-metric {
            transition: all 0.3s ease;
        }
        
        .performance-metric:hover {
            transform: scale(1.05);
        }
        
        .comment-card {
            transition: all 0.3s ease;
        }
        
        .comment-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .grade-badge {
            transition: all 0.3s ease;
        }
        
        .grade-badge:hover {
            transform: scale(1.1);
        }
        
        .student-avatar, .student-avatar-sm {
            transition: all 0.3s ease;
        }
        
        .student-avatar:hover, .student-avatar-sm:hover {
            transform: scale(1.1);
        }
        
        .btn-group .btn {
            transition: all 0.3s ease;
        }
        
        .btn-group .btn:hover {
            transform: translateY(-1px);
        }
        
        .event-card {
            transition: all 0.3s ease;
        }
        
        .event-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .table tbody tr {
            transition: all 0.3s ease;
        }
        
        .table tbody tr:hover {
            transform: translateX(2px);
        }
        
        .modal-content {
            animation: modalSlideIn 0.3s ease;
        }
        
        @keyframes modalSlideIn {
            from { opacity: 0; transform: translateY(-50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .form-control:focus, .form-select:focus {
            transform: scale(1.02);
            transition: all 0.3s ease;
        }
        
        .sidebar .nav-link {
            transition: all 0.3s ease;
        }
        
        .sidebar .nav-link:hover {
            padding-left: 1.5rem;
        }
        
        .classroom-info {
            transition: all 0.3s ease;
        }
        
        .classroom-info:hover {
            background: rgba(255, 255, 255, 0.15);
        }
    `
  document.head.appendChild(style)
})
