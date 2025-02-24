document.addEventListener("DOMContentLoaded", function () {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusDiv = document.getElementById('status');

    startBtn.addEventListener('click', function () {
        fetch('/start_listening', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            statusDiv.textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    stopBtn.addEventListener('click', function () {
        fetch('/stop_listening', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            statusDiv.textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
