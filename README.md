# SelfCraft Media Editor (SME)

An automated video post-production tool for SelfCraft Academy. Drop a raw
video into the right folder — SME transcribes it, burns captions, removes
silence, and exports a clean finished video. The original is never touched.

---

## What It Does

- Watches folders for new video files automatically
- Reads programme, week, module, and lesson info from the folder structure
- Transcribes audio using Whisper AI (runs fully offline)
- Burns captions onto the video at the correct size
- Exports Recorded Lessons in landscape (1920×1080) and Reels/Testimonials
  in vertical (1080×1920)
- Saves output as `Lesson Name (Edited).mp4` — never overwrites originals
- Browser-based dashboard with live progress updates

---

## Requirements

- Python 3.11 or newer
- FFmpeg
- Git

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/davidowoh/selfcraft-media-editor.git
cd selfcraft-media-editor
```

### 2. Create and activate a virtual environment

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install fastapi uvicorn openai-whisper watchdog python-multipart
```

### 4. Install FFmpeg

**Fedora Linux:**
```bash
sudo dnf install ffmpeg
```

**Ubuntu / Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
```bash
winget install ffmpeg
```

### 5. Install tkinter (for folder picker in Settings)

**Fedora Linux:**
```bash
sudo dnf install python3-tkinter
```

**Ubuntu / Debian:**
```bash
sudo apt install python3-tk
```

**Windows:** tkinter is included with Python by default.

---

## Configuration

Open `config/settings.json` and update the folder paths to match your machine:

```json
{
  "folders": {
    "raw_videos": "/your/path/to/SelfCraft Media/Raw Videos",
    "edited_videos": "/your/path/to/SelfCraft Media/Edited Videos",
    "temp": "/your/path/to/SelfCraft Media/Temp"
  },
  "file_manager": "nautilus",
  "captions": {
    "font": "Liberation Sans",
    "size": 14,
    "colour": "&H00FFFFFF",
    "outline_colour": "&H00000000",
    "outline": 2,
    "shadow": 1,
    "margin_bottom": 20
  },
  "whisper_model": "base",
  "max_parallel_jobs": 1
}
```

**Windows users:** use forward slashes or double backslashes in paths:
```json
"raw_videos": "C:/Users/YourName/SelfCraft Media/Raw Videos"
```

**File manager command:**
- Linux (GNOME): `nautilus`
- Linux (XFCE): `thunar`
- Linux (KDE): `dolphin`
- Windows: `explorer`

You can also change all folder paths from the Settings panel inside the
dashboard without editing this file manually.

---

## Folder Structure

Create this folder structure on your machine before running the app
(or configure different paths in Settings):

```
SelfCraft Media/
  Raw Videos/
    Recorded Classes/
      Programme Name/
        Week 1/
          Module 1/
            Lesson 1 - Title.mp4
    Teaching Reels/
    Testimonials/
  Edited Videos/
  Temp/
```

The folder names feed the metadata system directly — SME reads programme,
week, module, and lesson information from the path automatically.

---

## Running the App

### Start the server

```bash
source .venv/bin/activate   # Linux/macOS
# or
.venv\Scripts\activate      # Windows

uvicorn app.core.main:app --reload
```

### Open the dashboard

Open `dashboard.html` directly in your browser. On Linux:

```bash
xdg-open dashboard.html
```

Or drag the file into a browser window.

The dashboard connects to the server at `http://127.0.0.1:8000`.

---

## First Run

The first time Whisper runs it downloads the base model (~140 MB).
An internet connection is required once. After that, everything runs
fully offline.

---

## Using the Dashboard

| Button | What it does |
|---|---|
| ▶ Process | Run the full pipeline on this video |
| ↺ Re-run | Process again — creates a versioned copy (v2, v3…) |
| ↺ Retry | Re-attempt a failed job |
| ▶ Raw | Play the original unedited video |
| ▶ Edited | Play the latest edited output |
| 📂 Raw Videos | Open the Raw Videos folder in your file manager |
| 🎬 Edited Videos | Open the Edited Videos folder |
| 🗑 Clear Completed | Remove completed jobs from the list (files are kept) |
| ⚙️ Settings | Change folder paths, caption style, Whisper model |

---

## Supported Video Types

| Type | Folder | Output |
|---|---|---|
| Recorded Lesson | `Recorded Classes/` | 1920×1080 landscape |
| Teaching Reel | `Teaching Reels/` | 1080×1920 vertical |
| Testimonial | `Testimonials/` | 1080×1920 vertical |

---

## Troubleshooting

**Dashboard shows "Cannot reach backend"**
The server is not running. Start it with `uvicorn app.core.main:app --reload`.

**Video stuck on "processing" after restart**
Normal — the app detects this on startup and resets stuck jobs to "detected"
automatically.

**Captions not appearing**
Check that the `.srt` file was generated in the Temp folder during processing.
If the Temp folder is empty after a failed run, the transcription step failed —
check the terminal for Whisper errors.

**FFmpeg not found**
Run `ffmpeg -version` in your terminal. If it fails, reinstall FFmpeg and
make sure it is added to your PATH.

**Folder picker (Browse button) not working**
Install tkinter for your platform (see Installation step 5).

---

## Tech Stack

| Component | Tool |
|---|---|
| Backend | Python, FastAPI |
| Transcription | OpenAI Whisper (local, offline) |
| Video processing | FFmpeg |
| Database | SQLite |
| Folder watching | watchdog |
| Frontend | Plain HTML/CSS/JS (no framework) |

---

## Notes for Windows Users

- Change `file_manager` in settings to `explorer`
- Use the Settings panel Browse button to set folder paths
  (avoids backslash issues)
- The first Whisper model download requires an internet connection
- Everything else runs fully offline

---

*SelfCraft Academy — internal tooling*