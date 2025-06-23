document.addEventListener("DOMContentLoaded", () => {
  // Estado de la aplicación
  const state = {
    currentSection: "dashboard",
    searchTimeout: null,
    activeModal: null,
    filters: {
      estudiantes: { search: "", aula: "", sort: "nombre" },
      representantes: { search: "", estudiantes: "", aula: "" },
    },
  }

  // Cacheo de elementos del DOM
  const DOM = {
    navLinks: document.querySelectorAll(".nav-links .nav-item"),
    sections: document.querySelectorAll(".content-section"),
    globalSearch: document.getElementById("globalSearch"),
    sectionTitle: document.getElementById("sectionTitle"),
    currentSectionBreadcrumb: document.getElementById("currentSection"),
    refreshBtn: document.getElementById("refreshBtn"),
  }

  // Configuración de secciones
  const sectionsConfig = {
    dashboard: { title: "Dashboard", icon: "fas fa-tachometer-alt" },
    aulas: { title: "Gestión de Aulas", icon: "fas fa-school" },
    estudiantes: { title: "Gestión de Estudiantes", icon: "fas fa-child" },
    representantes: { title: "Gestión de Representantes", icon: "fas fa-users" },
    profesores: { title: "Gestión de Profesores", icon: "fas fa-chalkboard-teacher" },
    evaluaciones: { title: "Evaluaciones", icon: "fas fa-clipboard-check" },
    eventos: { title: "Eventos", icon: "fas fa-calendar-day" },
    reportes: { title: "Reportes", icon: "fas fa-chart-bar" },
  }

  // Inicialización
  function init() {
    setupNavigation()
    setupSearch()
    setupFilters()
    setupModals()
    setupFormValidation()
    setupEventListeners()
    setupActionButtons()
    showSection(state.currentSection)
    loadInitialData()

    console.log("Panel del director inicializado correctamente")
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

  // CONFIGURACIÓN DE BOTONES DE ACCIÓN -------------------------------
  function setupActionButtons() {
    // Botones de ver detalles
    document.querySelectorAll('[title="Ver estudiantes"], .btn-outline-info').forEach((btn) => {
      if (btn.onclick || btn.getAttribute("onclick")) return // Skip if already has onclick

      btn.addEventListener("click", function (e) {
        e.preventDefault()
        const card = this.closest(".card, tr")
        if (card) {
          const aulaId = this.getAttribute("data-aula-id") || extractIdFromContext(card)
          if (aulaId) {
            window.verEstudiantesAula(aulaId)
          } else {
            showNotification("No se pudo identificar el aula", "warning")
          }
        }
      })
    })

    // Botones de editar
    document.querySelectorAll('[title="Editar"], .btn-outline-warning').forEach((btn) => {
      if (btn.dataset.bsTarget) return // Skip modal triggers

      btn.addEventListener("click", function (e) {
        e.preventDefault()
        const itemType = detectItemType(this)
        const itemId = extractIdFromContext(this.closest(".card, tr"))

        if (itemType && itemId) {
          abrirModalEdicion(itemType, itemId)
        } else {
          showNotification("No se pudo identificar el elemento a editar", "warning")
        }
      })
    })

    // Botones de eliminar
    document.querySelectorAll('[title="Eliminar"], .btn-outline-danger').forEach((btn) => {
      if (btn.onclick || btn.getAttribute("onclick")) return // Skip if already has onclick

      btn.addEventListener("click", function (e) {
        e.preventDefault()
        const itemType = detectItemType(this)
        const itemId = extractIdFromContext(this.closest(".card, tr"))

        if (itemType && itemId) {
          window.confirmarEliminacion(itemType, itemId)
        } else {
          showNotification("No se pudo identificar el elemento a eliminar", "warning")
        }
      })
    })

    // Botones de contactar representante
    document.querySelectorAll(".btn-outline-primary").forEach((btn) => {
      if (btn.textContent.includes("Contactar") || btn.title === "Contactar") {
        btn.addEventListener("click", function (e) {
          e.preventDefault()
          const card = this.closest(".representante-item")
          if (card) {
            const email = extractEmailFromCard(card)
            const telefono = extractTelefonoFromCard(card)
            window.contactarRepresentante(email, telefono)
          }
        })
      }
    })

    // Botones de bloquear/desbloquear profesor
    document.querySelectorAll('[title="Bloquear"], [title="Desbloquear"]').forEach((btn) => {
      btn.addEventListener("click", function (e) {
        e.preventDefault()
        const profesorId = extractIdFromContext(this.closest("tr"))
        const accion = this.title.toLowerCase()

        if (profesorId) {
          window.cambiarEstadoProfesor(profesorId, accion)
        }
      })
    })
  }

  // FUNCIONES DE UTILIDAD PARA BOTONES -------------------------------
  function detectItemType(button) {
    const section = state.currentSection
    const card = button.closest(".card, tr")

    if (section === "aulas") return "aula"
    if (section === "estudiantes") return "estudiante"
    if (section === "representantes") return "representante"
    if (section === "profesores") return "profesor"
    if (section === "evaluaciones") return "evaluacion"
    if (section === "eventos") return "evento"

    // Detectar por clases CSS
    if (card) {
      if (card.classList.contains("student-profile-card")) return "estudiante"
      if (card.classList.contains("representante-item")) return "representante"
      if (card.classList.contains("event-card")) return "evento"
    }

    return null
  }

  function extractIdFromContext(element) {
    if (!element) return null

    // Buscar en atributos data-*
    const dataId = element.dataset.id || element.dataset.itemId
    if (dataId) return dataId

    // Buscar en el texto del elemento (para casos donde el ID esté visible)
    const text = element.textContent || element.innerText
    const idMatch = text.match(/ID:\s*(\d+)/) || text.match(/#(\d+)/)
    if (idMatch) return idMatch[1]

    // Buscar en elementos hijos con clases específicas
    const idElement = element.querySelector("[data-id], [data-item-id]")
    if (idElement) {
      return idElement.dataset.id || idElement.dataset.itemId
    }

    // Como último recurso, generar un ID temporal basado en el contenido
    const hash = simpleHash(element.textContent || "")
    return hash.toString()
  }

  function extractEmailFromCard(card) {
    const emailElement = card.querySelector('[href^="mailto:"]')
    if (emailElement) {
      return emailElement.href.replace("mailto:", "")
    }

    // Buscar por patrón de email en el texto
    const text = card.textContent || card.innerText
    const emailMatch = text.match(/[\w.-]+@[\w.-]+\.\w+/)
    return emailMatch ? emailMatch[0] : "No disponible"
  }

  function extractTelefonoFromCard(card) {
    // Buscar por patrón de teléfono venezolano
    const text = card.textContent || card.innerText
    const telefonoMatch = text.match(/04\d{2}-?\d{7}/) || text.match(/\d{10,11}/)
    return telefonoMatch ? telefonoMatch[0] : "No disponible"
  }

  function simpleHash(str) {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i)
      hash = (hash << 5) - hash + char
      hash = hash & hash // Convert to 32bit integer
    }
    return Math.abs(hash)
  }

  function abrirModalEdicion(tipo, id) {
    // Buscar modal específico para edición
    const modalId = `edit${tipo.charAt(0).toUpperCase() + tipo.slice(1)}Modal${id}`
    let modal = document.getElementById(modalId)

    if (!modal) {
      // Si no existe el modal específico, usar el modal genérico
      modal = document.getElementById(`editar${tipo.charAt(0).toUpperCase() + tipo.slice(1)}Modal`)
    }

    if (modal) {
      const bootstrapModal = new window.bootstrap.Modal(modal)
      bootstrapModal.show()
    } else {
      showNotification(`Modal de edición para ${tipo} no encontrado`, "warning")
    }
  }

  // BÚSQUEDA Y FILTRADO -----------------------------------------------
  function setupSearch() {
    if (DOM.globalSearch) {
      DOM.globalSearch.addEventListener("input", function () {
        clearTimeout(state.searchTimeout)
        state.searchTimeout = setTimeout(() => {
          performGlobalSearch(this.value.trim())
        }, 300)
      })
    }

    // Búsqueda específica de estudiantes
    const searchEstudiante = document.getElementById("searchEstudiante")
    if (searchEstudiante) {
      searchEstudiante.addEventListener("input", function () {
        clearTimeout(state.searchTimeout)
        state.searchTimeout = setTimeout(() => {
          state.filters.estudiantes.search = this.value.trim()
          filterEstudiantes()
        }, 300)
      })
    }

    // Búsqueda específica de representantes
    const searchRepresentante = document.getElementById("searchRepresentante")
    if (searchRepresentante) {
      searchRepresentante.addEventListener("input", function () {
        clearTimeout(state.searchTimeout)
        state.searchTimeout = setTimeout(() => {
          state.filters.representantes.search = this.value.trim()
          filterRepresentantes()
        }, 300)
      })
    }
  }

  function performGlobalSearch(query) {
    if (!query) {
      clearSearchHighlights()
      return
    }

    switch (state.currentSection) {
      case "representantes":
        state.filters.representantes.search = query
        filterRepresentantes()
        break
      case "estudiantes":
        state.filters.estudiantes.search = query
        filterEstudiantes()
        break
      default:
        // Buscar en estudiantes por defecto
        showSection("estudiantes")
        setTimeout(() => {
          state.filters.estudiantes.search = query
          filterEstudiantes()
        }, 100)
    }
  }

  function filterEstudiantes() {
    const cards = document.querySelectorAll(".estudiante-card")
    const filters = state.filters.estudiantes
    let visibleCount = 0

    cards.forEach((card) => {
      let shouldShow = true

      // Filtro por texto
      if (filters.search) {
        const nombre = card.dataset.nombre || ""
        if (!nombre.toLowerCase().includes(filters.search.toLowerCase())) {
          shouldShow = false
        }
      }

      // Filtro por aula
      if (filters.aula && shouldShow) {
        const aula = card.dataset.aula || ""
        if (aula !== filters.aula) {
          shouldShow = false
        }
      }

      card.style.display = shouldShow ? "block" : "none"
      if (shouldShow) {
        visibleCount++
        if (filters.search) highlightSearchTerm(card, filters.search)
      }
    })

    updateNoResultsMessage(visibleCount, "estudiantes")

    // Ordenar si es necesario
    if (filters.sort && visibleCount > 0) {
      sortEstudiantes(filters.sort)
    }
  }

  function filterRepresentantes() {
    const cards = document.querySelectorAll(".representante-card")
    const filters = state.filters.representantes
    let visibleCount = 0

    cards.forEach((card) => {
      let shouldShow = true

      // Filtro por texto
      if (filters.search) {
        const nombre = card.dataset.nombre || ""
        const cedula = card.dataset.cedula || ""
        const email = card.dataset.email || ""

        const searchText = `${nombre} ${cedula} ${email}`.toLowerCase()
        if (!searchText.includes(filters.search.toLowerCase())) {
          shouldShow = false
        }
      }

      // Filtro por número de estudiantes
      if (filters.estudiantes && shouldShow) {
        const numEstudiantes = Number.parseInt(card.dataset.estudiantes) || 0

        switch (filters.estudiantes) {
          case "1":
            if (numEstudiantes !== 1) shouldShow = false
            break
          case "2":
            if (numEstudiantes !== 2) shouldShow = false
            break
          case "3+":
            if (numEstudiantes < 3) shouldShow = false
            break
        }
      }

      card.style.display = shouldShow ? "block" : "none"
      if (shouldShow) {
        visibleCount++
        if (filters.search) highlightSearchTerm(card, filters.search)
      }
    })

    updateNoResultsMessage(visibleCount, "representantes")
  }

  function sortEstudiantes(sortValue) {
    const container = document.getElementById("estudiantesGrid")
    if (!container) return

    const cards = Array.from(container.querySelectorAll('.estudiante-card:not([style*="display: none"])'))

    cards.sort((a, b) => {
      switch (sortValue) {
        case "nombre":
          return a.dataset.nombre.localeCompare(b.dataset.nombre)
        case "apellido":
          return a.dataset.nombre.split(" ")[1]?.localeCompare(b.dataset.nombre.split(" ")[1]) || 0
        case "edad":
          return Number.parseInt(a.dataset.edad) - Number.parseInt(b.dataset.edad)
        case "aula":
          return a.dataset.aula.localeCompare(b.dataset.aula)
        default:
          return 0
      }
    })

    // Reordenar en el DOM
    cards.forEach((card) => container.appendChild(card))
  }

  // FILTROS AVANZADOS -------------------------------------------------
  function setupFilters() {
    // Filtros de estudiantes
    const filterAulaEstudiante = document.getElementById("filterAulaEstudiante")
    const sortEstudiantes = document.getElementById("sortEstudiantes")

    if (filterAulaEstudiante) {
      filterAulaEstudiante.addEventListener("change", function () {
        state.filters.estudiantes.aula = this.value
        filterEstudiantes()
      })
    }

    if (sortEstudiantes) {
      sortEstudiantes.addEventListener("change", function () {
        state.filters.estudiantes.sort = this.value
        filterEstudiantes()
      })
    }

    // Filtros de representantes
    const filterEstudiantes = document.getElementById("filterEstudiantes")
    const filterAula = document.getElementById("filterAula")
    const applyFilters = document.getElementById("applyFilters")

    if (filterEstudiantes) {
      filterEstudiantes.addEventListener("change", function () {
        state.filters.representantes.estudiantes = this.value
      })
    }

    if (filterAula) {
      filterAula.addEventListener("change", function () {
        state.filters.representantes.aula = this.value
      })
    }

    if (applyFilters) {
      applyFilters.addEventListener("click", filterRepresentantes)
    }
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
    // Validación de cédula
    document.querySelectorAll('input[name="cedula_representante"]').forEach((input) => {
      input.addEventListener("input", function () {
        const value = this.value.replace(/\D/g, "")
        this.value = value

        if (value.length < 7 || value.length > 8) {
          this.setCustomValidity("La cédula debe tener entre 7 y 8 dígitos")
        } else {
          this.setCustomValidity("")
        }
      })
    })

    // Validación de teléfono
    document.querySelectorAll('input[name="telefono_representante"]').forEach((input) => {
      input.addEventListener("input", function () {
        const value = this.value.replace(/\D/g, "")
        this.value = value

        if (value.length < 10 || value.length > 11) {
          this.setCustomValidity("El teléfono debe tener entre 10 y 11 dígitos")
        } else {
          this.setCustomValidity("")
        }
      })
    })

    // Validación de capacidad de aula
    document.querySelectorAll('input[name="capacidad"]').forEach((input) => {
      input.addEventListener("input", function () {
        const value = Number.parseInt(this.value)
        if (value < 1 || value > 50) {
          this.setCustomValidity("La capacidad debe estar entre 1 y 50 estudiantes")
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

    // Aplicar filtros de estudiantes
    const aplicarFiltrosBtn = document.querySelector('[onclick="aplicarFiltrosEstudiantes()"]')
    if (aplicarFiltrosBtn) {
      aplicarFiltrosBtn.onclick = () => {
        filterEstudiantes()
      }
    }
  }

  // DATOS Y CARGA -----------------------------------------------------
  function loadInitialData() {
    updateDashboardStats()
    loadRecentActivity()
    loadUpcomingEvents()
    initializeCharts()
  }

  function updateDashboardStats() {
    animateElements(".stats-card", 100)
  }

  function loadRecentActivity() {
    animateElements(".activity-item", 200)
  }

  function loadUpcomingEvents() {
    animateElements(".event-item", 200)
  }

  function loadSectionData(sectionName) {
    switch (sectionName) {
      case "representantes":
        animateElements(".representante-card", 100)
        setupActionButtons() // Re-setup buttons for new content
        break
      case "estudiantes":
        animateElements(".estudiante-card", 100)
        setupActionButtons()
        break
      case "profesores":
        animateElements("tbody tr", 50)
        setupActionButtons()
        break
      case "aulas":
        animateElements("tbody tr", 50)
        setupActionButtons()
        break
      case "eventos":
        animateElements(".event-card", 100)
        setupActionButtons()
        break
      case "reportes":
        initializeCharts()
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

  function initializeCharts() {
    // Gráfico de distribución por aulas
    const ctx = document.getElementById("aulasChart")
    if (ctx && typeof window.Chart !== "undefined") {
      new window.Chart(ctx, {
        type: "doughnut",
        data: {
          labels: ["Maternal", "Preescolar", "Primaria"],
          datasets: [
            {
              data: [12, 19, 8],
              backgroundColor: ["#ef4444", "#06b6d4", "#2563eb"],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      })
    }
  }

  // UTILIDADES --------------------------------------------------------
  function highlightSearchTerm(element, term) {
    const textElements = element.querySelectorAll("h6, .fw-bold, p:not(.text-muted)")
    const regex = new RegExp(`(${term})`, "gi")

    textElements.forEach((el) => {
      if (el.innerHTML.indexOf("<mark") === -1) {
        el.innerHTML = el.textContent.replace(regex, '<mark class="search-highlight">$1</mark>')
      }
    })
  }

  function clearSearchHighlights() {
    document.querySelectorAll(".search-highlight").forEach((el) => {
      el.replaceWith(el.textContent)
    })
  }

  function updateNoResultsMessage(visibleCount, section) {
    let noResultsDiv = document.getElementById(`no-results-${section}`)
    const grid = document.getElementById(`${section}Grid`) || document.querySelector(`#${section} .row`)

    if (visibleCount === 0 && grid) {
      if (!noResultsDiv) {
        noResultsDiv = document.createElement("div")
        noResultsDiv.id = `no-results-${section}`
        noResultsDiv.className = "col-12 text-center py-5"
        noResultsDiv.innerHTML = `
                    <div class="no-results-content">
                        <i class="fas fa-search fa-3x text-muted mb-3"></i>
                        <h5 class="text-muted">No se encontraron resultados</h5>
                        <p class="text-muted">Intenta ajustar los filtros de búsqueda</p>
                        <button class="btn btn-outline-primary" onclick="window.clearAllFilters('${section}')">
                            <i class="fas fa-times me-1"></i> Limpiar filtros
                        </button>
                    </div>
                `
        grid.appendChild(noResultsDiv)
      }
      noResultsDiv.style.display = "block"
    } else if (noResultsDiv) {
      noResultsDiv.style.display = "none"
    }
  }

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
  window.verEstudiantesAula = (aulaId) => {
    // Implementar lógica para mostrar estudiantes del aula
    const modal = new window.bootstrap.Modal(document.getElementById("estudiantesAulaModal"))

    // Aquí harías una petición AJAX para obtener los estudiantes
    document.getElementById("estudiantesAulaContent").innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando estudiantes del aula...</p>
            </div>
        `

    modal.show()

    // Simular carga de datos
    setTimeout(() => {
      document.getElementById("estudiantesAulaContent").innerHTML = `
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Edad</th>
                                <th>Representante</th>
                                <th>Teléfono</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Juan Pérez</td>
                                <td>5 años</td>
                                <td>María Pérez</td>
                                <td>0412-1234567</td>
                            </tr>
                            <tr>
                                <td>Ana García</td>
                                <td>4 años</td>
                                <td>Carlos García</td>
                                <td>0414-7654321</td>
                            </tr>
                            <tr>
                                <td>Luis Rodríguez</td>
                                <td>6 años</td>
                                <td>Carmen Rodríguez</td>
                                <td>0416-9876543</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            `
    }, 1000)
  }

  window.contactarRepresentante = (email, telefono) => {
    const modalHtml = `
            <div class="modal fade" id="contactModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <h5 class="modal-title">
                                <i class="fas fa-phone me-2"></i>
                                Contactar Representante
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="contact-info">
                                <div class="mb-3">
                                    <label class="form-label fw-bold">Email:</label>
                                    <div class="d-flex align-items-center">
                                        <span class="me-2">${email || "No disponible"}</span>
                                        ${
                                          email && email !== "No disponible"
                                            ? `<button class="btn btn-sm btn-outline-primary" onclick="window.copyToClipboard('${email}')">
                                            <i class="fas fa-copy"></i>
                                        </button>`
                                            : ""
                                        }
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-bold">Teléfono:</label>
                                    <div class="d-flex align-items-center">
                                        <span class="me-2">${telefono || "No disponible"}</span>
                                        ${
                                          telefono && telefono !== "No disponible"
                                            ? `<button class="btn btn-sm btn-outline-primary" onclick="window.copyToClipboard('${telefono}')">
                                            <i class="fas fa-copy"></i>
                                        </button>`
                                            : ""
                                        }
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                            ${
                              email && email !== "No disponible"
                                ? `<a href="mailto:${email}" class="btn btn-primary">
                                <i class="fas fa-envelope me-1"></i> Enviar Email
                            </a>`
                                : ""
                            }
                        </div>
                    </div>
                </div>
            </div>
        `

    // Remover modal anterior si existe
    const existingModal = document.getElementById("contactModal")
    if (existingModal) {
      existingModal.remove()
    }

    document.body.insertAdjacentHTML("beforeend", modalHtml)
    const modal = new window.bootstrap.Modal(document.getElementById("contactModal"))
    modal.show()
  }

  window.confirmarEliminacion = (tipo, id) => {
    const tipoTexto = {
      aula: "aula",
      estudiante: "estudiante",
      representante: "representante",
      profesor: "profesor",
      evaluacion: "evaluación",
      evento: "evento",
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

  window.cambiarEstadoProfesor = (id, accion) => {
    const textoAccion = accion === "bloquear" ? "bloquear" : "desbloquear"

    if (confirm(`¿Estás seguro de que deseas ${textoAccion} este profesor?`)) {
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
      actionInput.value = `${accion}_profesor`
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

  window.clearAllFilters = (section) => {
    switch (section) {
      case "estudiantes":
        const searchEst = document.getElementById("searchEstudiante")
        const filterAulaEst = document.getElementById("filterAulaEstudiante")
        const sortEst = document.getElementById("sortEstudiantes")

        if (searchEst) searchEst.value = ""
        if (filterAulaEst) filterAulaEst.value = ""
        if (sortEst) sortEst.value = "nombre"

        state.filters.estudiantes = { search: "", aula: "", sort: "nombre" }
        filterEstudiantes()
        break
      case "representantes":
        const searchRep = document.getElementById("searchRepresentante")
        const filterEstRep = document.getElementById("filterEstudiantes")
        const filterAulaRep = document.getElementById("filterAula")

        if (searchRep) searchRep.value = ""
        if (filterEstRep) filterEstRep.value = ""
        if (filterAulaRep) filterAulaRep.value = ""

        state.filters.representantes = { search: "", estudiantes: "", aula: "" }
        filterRepresentantes()
        break
    }

    clearSearchHighlights()
    showNotification("Filtros limpiados", "info")
  }

  window.copyToClipboard = (text) => {
    if (navigator.clipboard) {
      navigator.clipboard
        .writeText(text)
        .then(() => {
          showNotification("Copiado al portapapeles", "success")
        })
        .catch((err) => {
          console.error("Error al copiar:", err)
          showNotification("Error al copiar", "danger")
        })
    } else {
      // Fallback para navegadores que no soportan clipboard API
      const textArea = document.createElement("textarea")
      textArea.value = text
      document.body.appendChild(textArea)
      textArea.select()
      try {
        document.execCommand("copy")
        showNotification("Copiado al portapapeles", "success")
      } catch (err) {
        showNotification("Error al copiar", "danger")
      }
      document.body.removeChild(textArea)
    }
  }

  window.aplicarFiltrosEstudiantes = () => {
    filterEstudiantes()
  }

  // Exponer función showSection globalmente
  window.showSection = showSection

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
        
        .search-highlight {
            background-color: #fef3c7;
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: bold;
        }
        
        .notification-toast {
            border-left: 4px solid;
        }
        
        .student-avatar, .teacher-avatar, .aula-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--primary-color), var(--info-color));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .student-info .info-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }
        
        .event-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .event-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .stat-item h3 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
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
        
        .btn-group .btn {
            transition: all 0.3s ease;
        }
        
        .btn-group .btn:hover {
            transform: translateY(-1px);
        }
    `
  document.head.appendChild(style)
})
