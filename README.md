# YouTube Video Downloader with yt-dlp and Flask

This project allows you to download YouTube videos using the `yt-dlp` library. You can use this script either as a standalone command line tool or as a Flask web application.

## Prerequisites

Before you can use these scripts, make sure you have the following installed on your machine:

- Python 3.x: [Download Python](https://www.python.org/downloads/)
- yt-dlp: You can install this library using `pip`.
- Flask: You can install this library using `pip`.

## Installation

1. **Clone this repository** (if applicable) or download the scripts `download_video.py` and `app.py`.

2. **Install required libraries**:
    ```bash
    pip install yt-dlp Flask
    ```

## Usage

### Command Line Script

1. **Run the script**:
    ```bash
    python download_video.py
    ```

2. **Enter the YouTube video URL**:
    After running the script, it will prompt you to enter the URL of the YouTube video you want to download. Simply enter the URL in the console and press Enter.

### Flask Web Application

1. **Run the Flask app**:
    ```bash
    python app.py
    ```

2. **Open your web browser**:
    Go to `http://127.0.0.1:5000/` to access the web application.

3. **Enter the YouTube video URL**:
    In the web interface, enter the URL of the YouTube video you want to download and click the submit button. The video will be downloaded and you will be prompted to save the file.

## Example Codes

### Command Line Script: `download_video.py`

```python
# -*- coding: utf-8 -*-
import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download the best video and audio quality
        'outtmpl': '%(title)s.%(ext)s'  # Output file name template
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_video(video_url)
