# -*- coding: utf-8 -*-
import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Télécharge la meilleure qualité vidéo et audio
        'outtmpl': '%(title)s.%(ext)s'  # Nom du fichier de sortie
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Exemple d'utilisation
if __name__ == "__main__":
    video_url = input("Entrez l'URL de la vidéo YouTube : ")
    download_video(video_url)
