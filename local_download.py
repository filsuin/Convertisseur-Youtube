# -*- coding: utf-8 -*-
import yt_dlp
import re
import os

def download_media(url, format_choice, quality_choice):
    # Définir le chemin du dossier de sortie
    output_folder = os.path.join(os.getcwd(), "downloads")
    os.makedirs(output_folder, exist_ok=True)  # Crée le dossier s'il n'existe pas

    ydl_opts = {
        'format': f'bestvideo[height<={quality_choice}]+bestaudio/best' if format_choice.lower() == 'mp4' else 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s')  # Nom du fichier de sortie
    }

    if format_choice.lower() == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def is_valid_url(url):
    youtube_regex = (
        r'^(https?://)?(www\.)?'
        r'(youtube\.com|youtu\.?be)/.+$'
    )
    return re.match(youtube_regex, url) is not None

if __name__ == "__main__":
    while True:
        video_url = input("Entrez l'URL de la vidéo YouTube : ")
        if is_valid_url(video_url):
            break
        else:
            print("URL invalide. Veuillez entrer une URL YouTube valide.")

    while True:
        format_choice = input("Voulez-vous télécharger en format mp3 ou mp4 ? ").lower()
        if format_choice in ['mp3', 'mp4']:
            break
        else:
            print("Format invalide. Veuillez entrer 'mp3' ou 'mp4'.")

    # Choix de la qualité
    quality_choice = None
    if format_choice == 'mp4':
        while True:
            quality_choice = input("Choisissez la qualité vidéo (144, 240, 480, 720, 1080, 1440, 2160, 4320) : ")
            if quality_choice.isdigit():
                break
            else:
                print("Qualité invalide. Veuillez entrer une qualité vidéo valide (par exemple, 720 ou 1080).")

    download_media(video_url, format_choice, quality_choice)
    print(f"Le fichier a été téléchargé dans le dossier : {os.path.abspath('downloads')}")
