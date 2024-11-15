# -*- coding: utf-8 -*-
import yt_dlp

def download_media(url, format_choice):
    if format_choice.lower() == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Télécharge la meilleure qualité vidéo et audio
            'outtmpl': '%(title)s.%(ext)s'  # Nom du fichier de sortie
        }
    elif format_choice.lower() == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',  # Télécharge la meilleure qualité audio
            'outtmpl': '%(title)s.%(ext)s',  # Nom du fichier de sortie
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    else:
        print("Format non supporté. Veuillez choisir 'mp4' ou 'mp3'.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Exemple d'utilisation
if __name__ == "__main__":
    video_url = input("Entrez l'URL de la vidéo YouTube : ")
    format_choice = input("Voulez-vous télécharger en format mp3 ou mp4 ? ")
    download_media(video_url, format_choice)
