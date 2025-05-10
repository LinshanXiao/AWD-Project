document.addEventListener('DOMContentLoaded', function () {
    // Element references
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const selectFileBtn = document.getElementById('select-file-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const alertSuccess = document.getElementById('alert-success');
    const alertError = document.getElementById('alert-error');
    const alertWarning = document.getElementById('alert-warning');
    const results = document.getElementById('results');
    const addedCount = document.getElementById('added-count');
    const updatedCount = document.getElementById('updated-count');
    const errorCount = document.getElementById('error-count');
    const errorContainer = document.getElementById('error-container');
    const errorList = document.getElementById('error-list');
    const downloadTemplateBtn = document.getElementById('download-template');

    // File drag events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.add('highlight');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.remove('highlight');
        }, false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            fileInput.files = files;
            handleFile(files[0]);
        }
    }

    selectFileBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            handleFile(fileInput.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.name.endsWith('.csv')) {
            showAlert(alertError, 'Please upload a CSV file');
            return;
        }

        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.style.display = 'block';

        resetAlerts();
        results.style.display = 'none';
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    uploadBtn.addEventListener('click', () => {
        if (!fileInput.files.length) {
            showAlert(alertError, 'Please select a CSV file');
            return;
        }
        uploadFile(fileInput.files[0]);
    });

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const xhr = new XMLHttpRequest();
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressText.textContent = 'Uploading... 0%';

        resetAlerts();
        results.style.display = 'none';

        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = Math.round((e.loaded / e.total) * 100);
                progressBar.style.width = percentComplete + '%';
                progressText.textContent = `Uploading... ${percentComplete}%`;
            }
        });

        xhr.addEventListener('load', () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                const response = JSON.parse(xhr.responseText);

                if (response.message) {
                    showAlert(alertSuccess, response.message);
                    displayResults(response);
                } else if (response.error) {
                    showAlert(alertError, response.error);
                }

                // Optional: redirect to /visualisation after success
                // setTimeout(() => { window.location.href = '/visualisation'; }, 2500);

            } else {
                showAlert(alertError, `Upload failed. Status: ${xhr.status}`);
            }
            setTimeout(() => {
                progressContainer.style.display = 'none';
            }, 2000);
        });

        xhr.addEventListener('error', () => {
            showAlert(alertError, 'Network error during upload.');
            progressContainer.style.display = 'none';
        });

        xhr.addEventListener('abort', () => {
            showAlert(alertWarning, 'Upload was cancelled.');
            progressContainer.style.display = 'none';
        });

        xhr.open('POST', '/upload', true);
        xhr.send(formData);
    }

    function displayResults(data) {
        addedCount.textContent = data.games_added || 0;
        updatedCount.textContent = data.games_updated || 0;

        if (data.errors && data.errors.length > 0) {
            errorCount.textContent = data.errors.length;
            errorContainer.style.display = 'block';
            errorList.innerHTML = '';
            data.errors.forEach(error => {
                const li = document.createElement('li');
                li.textContent = error;
                errorList.appendChild(li);
            });
        } else {
            errorCount.textContent = '0';
            errorContainer.style.display = 'none';
        }

        results.style.display = 'block';
    }

    function showAlert(element, message) {
        element.textContent = message;
        element.style.display = 'block';

        if (element === alertSuccess) {
            setTimeout(() => {
                element.style.display = 'none';
            }, 5000);
        }
    }

    function resetAlerts() {
        alertSuccess.style.display = 'none';
        alertError.style.display = 'none';
        alertWarning.style.display = 'none';
    }

    downloadTemplateBtn.addEventListener('click', () => {
        window.location.href = '/upload/download-template';
    });
});
