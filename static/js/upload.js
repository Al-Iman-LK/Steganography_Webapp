document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const progressBar = document.getElementById('upload-progress');
    const uploadArea = document.getElementById('upload-area');

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        fileInput.files = e.dataTransfer.files;
        handleFileSelect(e.dataTransfer.files[0]);
    });

    // File selection handling
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    function handleFileSelect(file) {
        // Validate file type and size
        const validTypes = ['image/png', 'image/jpeg', 'video/mp4', 'audio/mp3', 'application/pdf'];
        if (!validTypes.includes(file.type)) {
            alert('Invalid file type. Please upload PNG, JPG, MP4, MP3, or PDF files.');
            return;
        }

        if (file.size > 10 * 1024 * 1024) { // 10MB limit
            alert('File size too large. Maximum size is 10MB.');
            return;
        }

        // Update UI to show selected file
        document.getElementById('selected-file').textContent = file.name;
    }

    // Form submission with progress tracking
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(uploadForm);

        fetch('/api/files/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                window.location.href = `/process/${data.id}/`;
            }
        })
        .catch(error => {
            console.error('Upload failed:', error);
            alert('Upload failed. Please try again.');
        });
    });

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
