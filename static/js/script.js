document.addEventListener("DOMContentLoaded", function () {
    let selectedFormat = "mp4"; // Format par défaut

    const formatButtons = document.querySelectorAll(".format-button");

    // Gestion des clics sur les boutons de format
    formatButtons.forEach(button => {
        button.addEventListener("click", function () {
            selectedFormat = this.id === "format-mp4" ? "mp4" : "mp3";
            document.getElementById("format-input").value = selectedFormat;

            // Ajout de la classe active sur le bouton sélectionné
            formatButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // Gestion du formulaire et de la barre de progression
    const form = document.getElementById("download-form");
    const progressContainer = document.getElementById("progress-container");
    const progressBar = document.getElementById("progress-bar");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // Empêche le rechargement de la page
        const formData = new FormData(form);
        progressContainer.style.display = "block";
        progressBar.style.width = "0%";

        // Envoie de la requête avec un suivi de progression
        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                let downloadProgress = 0;

                // Simule la progression du téléchargement
                const downloadInterval = setInterval(() => {
                    downloadProgress += 10;
                    progressBar.style.width = downloadProgress + "%";

                    if (downloadProgress >= 100) {
                        clearInterval(downloadInterval);
                        progressBar.style.width = "100%";
                    }
                }, 500);

                // Télécharge le fichier une fois le téléchargement terminé
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = `video.${selectedFormat}`; // Utilise le format choisi pour le nom du fichier
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
            } else {
                alert("Échec du téléchargement.");
            }
        } catch (error) {
            console.error("Erreur:", error);
            alert("Erreur lors du téléchargement.");
        }
    });
});
