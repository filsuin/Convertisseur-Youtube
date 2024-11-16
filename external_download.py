# external_download.py
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"  # Dossier pour stocker temporairement les fichiers

# Assurez-vous que le dossier de téléchargement existe
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Fonction pour télécharger la vidéo ou l'audio
def download_file(url, format_choice):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if format_choice == 'mp4' else 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Spécifie le chemin et le nom du fichier avec le titre de la vidéo
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': format_choice
        }] if format_choice == 'mp3' else None
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            file_ext = 'mp3' if format_choice == 'mp3' else 'mp4'
            file_title = info_dict.get('title', 'file').replace("/", "_")  # Remplace les caractères interdits dans le nom du fichier
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{file_title}.{file_ext}")
            if os.path.exists(file_path):
                return file_path
            else:
                return None
        except Exception as e:
            print(f"Erreur lors du téléchargement : {e}")
            return None

# Route principale
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        format_choice = request.form.get("format", "mp4")  # MP4 par défaut

        if url:
            file_path = download_file(url, format_choice)
            if file_path:
                @after_this_request
                def remove_file(response):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Erreur lors de la suppression du fichier : {e}")
                    return response
                
                return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
            else:
                return jsonify({'error': 'Impossible de télécharger le fichier.'}), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
