# external_download.py
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"  # Dossier pour stocker temporairement les vidéos

# Assurez-vous que le dossier de téléchargement existe
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Fonction pour télécharger la vidéo et obtenir son chemin
def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Spécifie le chemin et le nom du fichier
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)  # Télécharge la vidéo
            video_title = info_dict.get('title', 'video')  # Récupère le titre pour nommer le fichier
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp4")
            if os.path.exists(file_path):
                return file_path  # Retourne le chemin du fichier téléchargé
            else:
                return None
        except Exception as e:
            print(f"Erreur lors du téléchargement de la vidéo : {e}")
            return None

# Route pour gérer la requête de téléchargement
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            # Télécharger la vidéo et obtenir le chemin du fichier
            file_path = download_video(url)
            if file_path:
                # Définir un nettoyage après l'envoi du fichier
                @after_this_request
                def remove_file(response):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Erreur lors de la suppression du fichier : {e}")
                    return response
                
                # Envoie du fichier au client pour téléchargement
                return send_file(file_path, as_attachment=True)
            else:
                return jsonify({'error': 'Impossible de télécharger la vidéo.'}), 500
    return render_template("index.html")

# Exécution du serveur
if __name__ == "__main__":
    app.run(debug=True)
