# YouTube Video Downloader with yt-dlp and Flask

This project allows you to download YouTube videos using the `yt-dlp` library. You can use this script either as a standalone command-line tool or as a Flask web application.

---

## **Prerequisites**

Before you can use these scripts, make sure you have the following installed on your machine:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **yt-dlp**: You can install this library using `pip`.
- **Flask**: You can install this library using `pip`.
- **Google API Key**: Required for the search functionality.

---

## **Setting Up Your Google API Key**

To enable the search functionality, you need a YouTube Data API key:

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.

2. **Enable the YouTube Data API v3**:
   - In the "APIs & Services" menu, select "Enable APIs and Services".
   - Search for "YouTube Data API v3" and enable it.

3. **Generate an API Key**:
   - Go to "Credentials" in the "APIs & Services" menu.
   - Click on "Create Credentials" > "API Key".
   - Copy the generated key.

4. **Secure the API Key** (optional but recommended):
   - Under "API restrictions," limit usage to the YouTube Data API.
   - Under "Application restrictions," restrict usage to your IP address or domain (for web apps).

---

## **Installation**

1. **Clone this repository** (if applicable) or download the scripts `local_download.py` and `external_dowload.py`.

2. **Install required libraries**:
    ```bash
    pip install yt-dlp Flask python-dotenv
    ```

3. **Set up the `.env` file**:
   - Create a file named `.env` in the root directory of your project.
   - Add the following line, replacing `YOUR_API_KEY` with your actual API key:
     ```env
     YOUTUBE_API_KEY=YOUR_API_KEY
     ```

   Make sure the `.env` file is added to your `.gitignore` to prevent accidental exposure.

---

## **Usage**

### **Command Line Script**

1. **Run the script**:
    ```bash
    python local_download.py
    ```

2. **Enter the YouTube video URL**:
    After running the script, it will prompt you to enter the URL of the YouTube video you want to download. Simply enter the URL in the console and press Enter.

3. **Search for videos (if enabled)**:
    Type your search query when prompted, and the script will return a list of video titles and links.

---

### **Flask Web Application**

1. **Run the Flask app**:
    ```bash
    python external_dowload.py
    ```

2. **Open your web browser**:
    Go to `http://127.0.0.1:5000/` to access the web application.

3. **Search or Enter the YouTube video URL**:
    - Use the search bar to find videos by typing a query. Results will appear dynamically as you type.
    - Select a video or paste the video URL into the input box.

4. **Download the video**:
    Click the "Download" button to download the video in your chosen format (MP3 or MP4).

5. **Open the file location**:
    Once the download is complete, click the button to open the folder where the file is saved.

---

## **Security Note**

- Ensure your API key is **not shared publicly**.
- If you accidentally expose your key, revoke it immediately in the Google Cloud Console and generate a new one.

---

Feel free to contribute or suggest improvements!
