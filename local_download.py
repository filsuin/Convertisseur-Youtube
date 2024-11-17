# -*- coding: utf-8 -*-
import yt_dlp
import re
import os


def list_available_formats(url, format_choice):
    """
    Liste les formats disponibles pour une URL donnée, en fonction du type choisi (mp4 ou mp3).
    """
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        format_options = []

        for fmt in formats:
            ext = fmt.get('ext', 'unknown')
            if ext == 'webm':  # Exclure les formats WebM
                continue

            if format_choice == "mp4" and fmt.get('vcodec') != 'none':  # Formats vidéo
                resolution = fmt.get('resolution', 'Inconnue')
                note = fmt.get('format_note', '')
                size = fmt.get('filesize')

                # Taille sécurisée
                size_str = f"{size / 1e6:.2f} MB" if size and isinstance(size, (int, float)) else "Inconnue"

                format_options.append({
                    'id': fmt.get('format_id'),
                    'resolution': resolution,
                    'ext': ext,
                    'note': note,
                    'size': size_str
                })

            elif format_choice == "mp3" and fmt.get('vcodec') == 'none':  # Formats audio uniquement
                size = fmt.get('filesize')
                bitrate = fmt.get('abr', 'Inconnu')  # Bitrate audio

                # Taille sécurisée
                size_str = f"{size / 1e6:.2f} MB" if size and isinstance(size, (int, float)) else "Inconnue"

                format_options.append({
                    'id': fmt.get('format_id'),
                    'resolution': "Audio uniquement",
                    'ext': ext,
                    'note': f"{bitrate}kbps",
                    'size': size_str
                })

        return format_options


def download_media(url, format_id, format_choice):
    """
    Télécharge la vidéo ou l'audio au format sélectionné.
    """
    output_folder = os.path.join(os.getcwd(), "downloads")
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        'format': format_id,  # Utiliser le format choisi par l'utilisateur
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Nom du fichier de sortie
        'merge_output_format': 'mp4' if format_choice == "mp4" else None  # S'assurer que les fichiers vidéo et audio sont fusionnés en MP4
    }

    # Ajout du postprocesseur pour MP3 si nécessaire
    if format_choice == "mp3":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def is_valid_url(url):
    """
    Vérifie si l'URL fournie est une URL YouTube valide.
    """
    youtube_regex = (
        r'^(https?://)?(www\.)?'
        r'(youtube\.com|youtu\.?be)/.+$'
    )
    return re.match(youtube_regex, url) is not None


if __name__ == "__main__":
    # Saisie de l'URL
    while True:
        video_url = input("Entrez l'URL de la vidéo YouTube : ")
        if is_valid_url(video_url):
            break
        else:
            print("URL invalide. Veuillez entrer une URL YouTube valide.")

    # Choix du format MP4 ou MP3
    while True:
        format_choice = input("Voulez-vous télécharger en format 'mp4' (vidéo) ou 'mp3' (audio) ? ").lower()
        if format_choice in ['mp4', 'mp3']:
            break
        else:
            print("Format invalide. Veuillez entrer 'mp4' ou 'mp3'.")

    # Afficher les formats disponibles
    print("Récupération des formats disponibles...")
    formats = list_available_formats(video_url, format_choice)
    if not formats:
        print("Aucun format disponible pour ce type.")
        exit()

    print("Formats disponibles :")
    for idx, fmt in enumerate(formats, start=1):
        print(f"{idx}. ID: {fmt['id']}, Résolution: {fmt['resolution']}, Format: {fmt['ext']}, "
              f"Note: {fmt['note']}, Taille: {fmt['size']}")

    # Sélection du format
    while True:
        try:
            choice = int(input("Choisissez un format en entrant son numéro : "))
            if 1 <= choice <= len(formats):
                selected_format = formats[choice - 1]
                break
            else:
                print("Numéro invalide, veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

    print(f"Vous avez choisi : Résolution {selected_format['resolution']}, Format {selected_format['ext']}")

    # Télécharger le fichier
    download_media(video_url, selected_format['id'], format_choice)
    print(f"Le fichier a été téléchargé dans le dossier : {os.path.abspath('downloads')}")
