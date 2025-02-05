document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('message-form');
    const statusElement = document.getElementById('status');

    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData();
            formData.append('message', document.getElementById('message').value);
            const fileId = messageForm.dataset.fileId;

            // Update UI to show processing state
            statusElement.textContent = 'Processing...';

            fetch(`/api/files/${fileId}/process/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: document.getElementById('message').value
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Processing failed');
                    });
                }
                return response.json();
            })
            .then(data => {
                window.location.href = '/files/';
            })
            .catch(error => {
                console.error('Processing failed:', error);
                statusElement.textContent = 'Processing failed: ' + error.message;
            });
        });
    }

    // CSRF token helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
