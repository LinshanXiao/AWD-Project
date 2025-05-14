document.addEventListener('DOMContentLoaded', function () {
    // --- DOM elements ---
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
    const csvAlertSuccess = document.getElementById('csv-alert-success');
    const csvAlertError = document.getElementById('csv-alert-error');
    const csvAlertWarning = document.getElementById('csv-alert-warning');
    const results = document.getElementById('results');
    const addedCount = document.getElementById('added-count');
    const updatedCount = document.getElementById('updated-count');
    const errorCount = document.getElementById('error-count');
    const errorContainer = document.getElementById('error-container');
    const errorList = document.getElementById('error-list');
    const downloadTemplateBtn = document.getElementById('download-template');

    // --- drag csvfile into the section processing ---
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
        }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => uploadArea.classList.add('highlight'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('highlight'), false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            handleFile(files[0]);
        }
    }

    selectFileBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            handleFile(fileInput.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.name.toLowerCase().endsWith('.csv')) {
        showAlert(csvAlertError, 'Please upload a CSV file');
        return;
        }
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.style.display = 'block';
        resetAlerts(csvAlertSuccess, csvAlertError, csvAlertWarning);
        results.style.display = 'none';
    }

    function formatFileSize(bytes) {
        const k = 1024, sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    uploadBtn.addEventListener('click', () => {
        if (!fileInput.files.length) {
            showAlert(csvAlertError, 'Please select a CSV file');
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

        resetAlerts(csvAlertSuccess, csvAlertError, csvAlertWarning);
        results.style.display = 'none';

        xhr.upload.addEventListener('progress', e => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                progressBar.style.width = percent + '%';
                progressText.textContent = `Uploading... ${percent}%`;
            }
        });

        xhr.onload = () => {
            const response = JSON.parse(xhr.responseText);
            if (xhr.status >= 200 && xhr.status < 300) {
                if (response.message) {
                    showAlert(csvAlertSuccess, response.message);
                    displayResults(response);
                    fileInput.value = '';
                    fileInfo.style.display = 'none';
                } else {
                    showAlert(csvAlertError, response.error || 'Unknown error');
                }
            } else {
                showAlert(csvAlertError, `Upload failed. Status: ${xhr.status}`);
            }
            setTimeout(() => progressContainer.style.display = 'none', 2000);
        };

        xhr.onerror = () => {
            showAlert(csvAlertError, 'Network error during upload.');
            progressContainer.style.display = 'none';
        };

        xhr.onabort = () => {
            showAlert(csvAlertWarning, 'Upload was cancelled.');
            progressContainer.style.display = 'none';
        };

        xhr.open('POST', '/upload/csv');
        xhr.send(formData);
    }

    function displayResults(data) {
    addedCount.textContent = data.rows_added || 0;
    updatedCount.textContent = 0;

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

    downloadTemplateBtn.addEventListener('click', () => {
        window.location.href = '/upload/download-template';
    });

    // --- manually input logic  ---
    const manualForm = document.getElementById('manual-form');
    const manualAlertSuccess = document.getElementById('manual-alert-success');
    const manualAlertError = document.getElementById('manual-alert-error');

    if (manualForm) {
        manualForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = {
                game_id: document.getElementById("game_id").value,
                date_played: document.getElementById("date_played").value,
                game_duration: document.getElementById("game_duration").value,
                winning_team: document.getElementById("winning_team").value,
                league_username: document.getElementById("league_username").value,
                champion: document.getElementById("champion").value,
                kills: document.getElementById("kills").value,
                deaths: document.getElementById("deaths").value,
                assists: document.getElementById("assists").value,
                team: document.getElementById("team").value
            };

            resetAlerts(manualAlertSuccess, manualAlertError);

            fetch("/upload/manual", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            })
                .then(res => res.json().then(data => ({ status: res.status, body: data })))
                .then(result => {
                    if (result.status === 200) {
                        showAlert(manualAlertSuccess, result.body.message || "Upload successful!");
                        manualForm.reset();
                    } else {
                        const details = result.body.details || result.body.error;
                        if (typeof details === "object") {
                            const formatted = Object.entries(details)
                                .map(([k, v]) => `${k}: ${v}`).join('\n');
                            showAlert(manualAlertError, `Upload failed:\n${formatted}`);
                        } else {
                            showAlert(manualAlertError, `Upload failed: ${details}`);
                        }
                    }
                })
                .catch(err => showAlert(manualAlertError, `Unexpected error: ${err}`));
        });
    }

    // --- shared alter function, both for upload csv file and input data---
    function showAlert(element, message) {
        element.textContent = message;
        element.style.display = 'block';
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }

    function resetAlerts(...elements) {
        elements.forEach(el => el && (el.style.display = 'none'));
    }
});
