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

    // Gestion de la soumission du formulaire
    document.getElementById("download-form").addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(this);

        fetch("/", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error("Erreur lors du téléchargement.");
            }
        })
        .then(blob => {
            const downloadUrl = URL.createObjectURL(blob);
            const a = document.getElementById("download-link");
            a.style.display = "block";
            a.href = downloadUrl;
            a.download = `video.${selectedFormat}`;
            a.click();
        })
        .catch(error => {
            console.error("Erreur :", error);
            alert("Une erreur est survenue lors du téléchargement.");
        });
    });
});
