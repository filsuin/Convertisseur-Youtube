# -*- coding: utf-8 -*-
import yt_dlp
import re
import os
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, StringVar, END
import requests

# Remplacez par votre clé API YouTube
API_KEY = "AIzaSyCFtYhGAnQ8vur2FGnQkkZkhLW2qkmnM8U"

def search_youtube(query):
    """Recherche de vidéos YouTube à partir d'une requête"""
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=10&q={query}&key={API_KEY}"
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json()
        videos = []
        for item in results.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            videos.append((title, f"https://www.youtube.com/watch?v={video_id}"))
        return videos
    else:
        messagebox.showerror("Erreur", "Impossible de récupérer les résultats de recherche.")
        return []

def on_search_button_click():
    """Effectuer une recherche et afficher les résultats"""
    query = search_entry.get()
    if not query:
        messagebox.showerror("Erreur", "Veuillez entrer une recherche.")
        return
    
    search_results.delete(0, END)  # Clear previous results
    videos = search_youtube(query)
    for title, url in videos:
        search_results.insert(END, f"{title} - {url}")

def on_result_select(event):
    """Préremplit le champ URL avec le lien sélectionné dans les résultats"""
    selected_item = search_results.get(search_results.curselection())
    video_url = selected_item.split(" - ")[-1]
    url_entry.delete(0, END)
    url_entry.insert(0, video_url)

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
root.title("Téléchargeur YouTube avec Recherche")

# Section Recherche
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Rechercher des vidéos YouTube :")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Rechercher", command=on_search_button_click)
search_button.pack(side=tk.LEFT, padx=5)

# Liste des résultats de recherche
results_frame = tk.Frame(root)
results_frame.pack(pady=10)

scrollbar = Scrollbar(results_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

search_results = Listbox(results_frame, width=80, height=10, yscrollcommand=scrollbar.set)
search_results.pack(side=tk.LEFT)
scrollbar.config(command=search_results.yview)

search_results.bind("<<ListboxSelect>>", on_result_select)

# Section Téléchargement
url_label = tk.Label(root, text="Entrez l'URL de la vidéo YouTube :")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

format_label = tk.Label(root, text="Choisissez le format (mp3 ou mp4) :")
format_label.pack(pady=5)

format_var = tk.StringVar(value="mp4")

mp3_button = tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3")
mp3_button.pack(pady=5)
mp4_button = tk.Radiobutton(root, text="MP4", variable=format_var, value="mp4")
mp4_button.pack(pady=5)

download_button = tk.Button(root, text="Télécharger", command=on_download_button_click)
download_button.pack(pady=20)

# Lancer l'application Tkinter
root.mainloop()
