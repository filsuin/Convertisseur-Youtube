document.getElementById("downloadForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const urlInput = document.getElementById("url");
    const url = urlInput.value;

    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({ url: url })
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error("Erreur lors du téléchargement de la vidéo");
        }
    })
    .then(blob => {
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = "video.mp4";
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(downloadUrl);
    })
    .catch(error => {
        console.error("Erreur :", error);
        alert("Une erreur est survenue lors de la récupération du lien.");
    });
});
