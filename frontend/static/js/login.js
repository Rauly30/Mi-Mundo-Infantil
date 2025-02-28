document.addEventListener('DOMContentLoaded', () => {
    setupAlerts();
});

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
