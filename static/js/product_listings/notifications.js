// WebSocket Notifications
function initNotifications() {
    const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    const notificationSocket = new WebSocket(
        ws_scheme + '://' + window.location.host + '/ws/notifications/'
    );

    notificationSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        showToast(data.message);
    };
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast fade-in';
    toast.innerHTML = `
        <div class="toast-body">
            <i class="fas fa-bell me-2"></i>${message}
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}
