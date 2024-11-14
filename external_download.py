# external_download.py
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

# Fonction pour obtenir le lien direct de téléchargement
def get_video_url(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Sélectionner la meilleure qualité vidéo et audio
        'noplaylist': True  # Ne pas télécharger de playlists
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)  # Obtenir les informations sans télécharger
            # Vérifier si le lien direct est disponible
            if 'url' in info_dict and info_dict.get('ext') in ['mp4', 'mkv', 'webm']:
                return info_dict['url']
            # Sinon, parcourir les formats pour trouver une URL vidéo
            elif 'formats' in info_dict:
                for format in info_dict['formats']:
                    # Sélectionner uniquement les formats vidéo
                    if 'url' in format and format.get('vcodec') != 'none' and format.get('ext') in ['mp4', 'mkv', 'webm']:
                        return format['url']
            else:
                return None  # Aucun lien vidéo trouvé
        except Exception as e:
            print(f"Erreur lors de la récupération du lien : {e}")
            return None

# Route pour traiter la requête de téléchargement
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            # Obtenir le lien direct de téléchargement
            download_url = get_video_url(url)
            if download_url:
                return jsonify({'download_url': download_url})  # Retourner le lien au client
            else:
                return jsonify({'error': 'Impossible de récupérer le lien de téléchargement.'}), 500
    return render_template("index.html")

# Exécution du serveur
if __name__ == "__main__":
    app.run(debug=True)
