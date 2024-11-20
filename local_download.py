# -*- coding: utf-8 -*-
import yt_dlp
import re
import os
import tkinter as tk
from tkinter import messagebox

def download_media(url, format_choice):
    # Définir le chemin du dossier de sortie
    output_folder = os.path.join(os.getcwd(), "downloads")
    os.makedirs(output_folder, exist_ok=True)  # Crée le dossier s'il n'existe pas

    if format_choice.lower() == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Télécharge la meilleure qualité vidéo et audio
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s')  # Nom du fichier de sortie
        }
    elif format_choice.lower() == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',  # Télécharge la meilleure qualité audio
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Nom du fichier de sortie
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    else:
        messagebox.showerror("Erreur", "Format non supporté. Veuillez choisir 'mp4' ou 'mp3'.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def is_valid_url(url):
    youtube_regex = (
        r'^(https?://)?(www\.)?'
        r'(youtube\.com|youtu\.?be)/.+$'
    )
    return re.match(youtube_regex, url) is not None

def on_download_button_click():
    video_url = url_entry.get()
    format_choice = format_var.get()

    if not is_valid_url(video_url):
        messagebox.showerror("Erreur", "URL invalide. Veuillez entrer une URL YouTube valide.")
        return

    if format_choice not in ['mp3', 'mp4']:
        messagebox.showerror("Erreur", "Format invalide. Veuillez choisir 'mp3' ou 'mp4'.")
        return

    download_media(video_url, format_choice)
    messagebox.showinfo("Succès", f"Le fichier a été téléchargé dans le dossier : {os.path.abspath('downloads')}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Téléchargeur YouTube")

# Label pour l'URL
url_label = tk.Label(root, text="Entrez l'URL de la vidéo YouTube :")
url_label.pack(pady=5)

# Champ de saisie pour l'URL
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Label pour le choix du format
format_label = tk.Label(root, text="Choisissez le format (mp3 ou mp4) :")
format_label.pack(pady=5)

# Variable pour le format choisi
format_var = tk.StringVar(value="mp4")

# Radiobuttons pour choisir entre mp3 ou mp4
mp3_button = tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3")
mp3_button.pack(pady=5)
mp4_button = tk.Radiobutton(root, text="MP4", variable=format_var, value="mp4")
mp4_button.pack(pady=5)

# Bouton pour lancer le téléchargement
download_button = tk.Button(root, text="Télécharger", command=on_download_button_click)
download_button.pack(pady=20)

# Lancer l'application Tkinter
root.mainloop()
