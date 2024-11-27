# -*- coding: utf-8 -*-
import yt_dlp
import re
import os
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END, ttk
import requests
import threading

# Remplacez par votre clé API YouTube
API_KEY = "AIzaSyCIcIEKn4zLObxDjW9sgvY8xjc24knZ3GQ"

# Cache pour les résultats
cache = {}

# Timer pour la temporisation
search_timer = None

def search_youtube(query):
    """Recherche de vidéos YouTube avec mise en cache."""
    if query in cache:
        return cache[query]  # Retourne les résultats mis en cache
    
    # Effectuer la requête API si les résultats ne sont pas en cache
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=10&fields=items(id(videoId),snippet(title))&q={query}&key={API_KEY}"
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json()
        videos = []
        for item in results.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            videos.append((title, f"https://www.youtube.com/watch?v={video_id}"))
        
        cache[query] = videos  # Mise en cache des résultats
        return videos
    else:
        return []

def update_suggestions_in_thread(query):
    """Effectue la recherche dans un thread séparé et met à jour les suggestions."""
    videos = search_youtube(query)
    search_results.delete(0, END)  # Efface les anciennes suggestions
    for title, url in videos:
        search_results.insert(END, f"{title} - {url}")

def update_suggestions(event):
    """Met à jour les suggestions avec temporisation et longueur minimale."""
    global search_timer
    query = search_entry.get().strip()
    
    # Si la requête est trop courte, effacer les résultats
    if len(query) < 3:
        search_results.delete(0, END)
        return

    # Annuler le précédent timer
    if search_timer:
        search_timer.cancel()

    # Démarrer un nouveau timer (300 ms)
    search_timer = threading.Timer(0.3, lambda: threading.Thread(target=update_suggestions_in_thread, args=(query,), daemon=True).start())
    search_timer.start()

def on_result_select(event):
    """Préremplit le champ URL avec le lien sélectionné dans les résultats."""
    if search_results.curselection():
        selected_item = search_results.get(search_results.curselection())
        video_url = selected_item.split(" - ")[-1]
        url_entry.delete(0, END)
        url_entry.insert(0, video_url)

def progress_hook(d):
    """Met à jour la barre de progression en fonction de l'état."""
    if d['status'] == 'downloading':
        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        downloaded = d.get('downloaded_bytes', 0)
        if total > 0:
            progress_value = int(downloaded / total * 100)
            progress_bar['value'] = progress_value
            progress_label.config(text=f"Téléchargement : {progress_value}%")
            root.update_idletasks()
    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        progress_label.config(text="Téléchargement terminé.")
        root.update_idletasks()

def download_media(url, format_choice):
    """Télécharge le média YouTube au format spécifié."""
    output_folder = os.path.join(os.getcwd(), "downloads")
    os.makedirs(output_folder, exist_ok=True)  # Crée le dossier s'il n'existe pas

    if format_choice.lower() == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook]
        }
    elif format_choice.lower() == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook]
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
    """Gère le clic sur le bouton de téléchargement."""
    video_url = url_entry.get()
    format_choice = format_var.get()

    if not is_valid_url(video_url):
        messagebox.showerror("Erreur", "URL invalide. Veuillez entrer une URL YouTube valide.")
        return

    if format_choice not in ['mp3', 'mp4']:
        messagebox.showerror("Erreur", "Format invalide. Veuillez choisir 'mp3' ou 'mp4'.")
        return

    # Réinitialiser la barre de progression
    progress_bar['value'] = 0
    progress_label.config(text="Téléchargement : 0%")

    # Lancer le téléchargement dans un thread séparé
    threading.Thread(target=download_media, args=(video_url, format_choice), daemon=True).start()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Téléchargeur YouTube")

# Section Recherche
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Rechercher des vidéos YouTube :")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)

search_entry.bind("<KeyRelease>", update_suggestions)

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

# Barre de progression
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=5)

progress_label = tk.Label(root, text="Téléchargement : 0%")
progress_label.pack(pady=5)

# Lancer l'application Tkinter
root.mainloop()
