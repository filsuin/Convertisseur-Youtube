from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Fonction de téléchargement de la vidéo
def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Télécharge la meilleure qualité vidéo et audio
        'outtmpl': output_path  # Nom du fichier de sortie
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(result)  # Le chemin réel du fichier téléchargé
    return video_filename

# Page d'accueil avec le formulaire
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")  # Récupère l'URL de la vidéo depuis le formulaire
        if url:
            # Définir le chemin de sortie du fichier téléchargé
            if not os.path.exists("downloads"):
                os.makedirs("downloads")  # Créer le dossier downloads si nécessaire

            output_path = "downloads/%(title)s.%(ext)s"
            downloaded_file = download_video(url, output_path)
            return send_file(downloaded_file, as_attachment=True)
    return render_template("index.html")

# Exécution du serveur
if __name__ == "__main__":
    app.run(debug=True)
