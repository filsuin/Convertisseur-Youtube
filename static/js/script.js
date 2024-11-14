// script.js
const form = document.getElementById("download-form");
const downloadLink = document.getElementById("download-link");

form.addEventListener("submit", async (e) => {
    e.preventDefault();  // Empêche le rechargement de la page

    const url = document.getElementById("url").value;
    const formData = new FormData();
    formData.append("url", url);

    try {
        // Envoyer la requête pour obtenir le lien direct
        const response = await fetch("/", {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        if (data.download_url) {
            downloadLink.href = data.download_url;  // Définit le lien de téléchargement direct
            downloadLink.style.display = "block";  // Rendre le lien visible
        } else {
            alert("Erreur lors de la récupération du lien de téléchargement.");
        }
    } catch (error) {
        console.error("Erreur:", error);
        alert("Une erreur est survenue lors de la récupération du lien.");
    }
});
