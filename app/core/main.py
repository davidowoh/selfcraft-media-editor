import os
import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database.db import (delete_video, get_all_videos, get_video_by_id, update_status,
                          reset_stuck_jobs, add_video, delete_completed,
                          update_progress)
from app.media.metadata import extract_metadata
from app.workflow.orchestrator import process_video

RAW_VIDEOS_FOLDER = "/home/davidowoh/SelfCraft Media/Raw Videos"

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith(('.mp4', '.mov')):
            print(f"Watcher detected: {event.src_path}")
            metadata = extract_metadata(event.src_path)
            add_video(event.src_path, metadata)

    def on_deleted(self, event):
        if event.src_path.lower().endswith(('.mp4', '.mov')):
            print(f"Watcher noticed deletion: {event.src_path}")
            from database.db import delete_by_filepath
            delete_by_filepath(event.src_path)

def start_watcher():
    observer = Observer()
    observer.schedule(VideoHandler(), RAW_VIDEOS_FOLDER, recursive=True)
    observer.start()
    print(f"Watcher started: {RAW_VIDEOS_FOLDER}")
    try:
        while True:
            time.sleep(2)
    except Exception:
        observer.stop()
    observer.join()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("SME starting up — checking for stuck jobs...")
    reset_stuck_jobs()
    watcher_thread = threading.Thread(target=start_watcher, daemon=True)
    watcher_thread.start()
    yield
    print("SME shutting down.")

app = FastAPI(title="SME Local API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/videos")
def list_videos():
    rows = get_all_videos()
    return [
        {
            "id": r[0],
            "filepath": r[1],
            "programme": r[2],
            "week": r[3],
            "module": r[4],
            "lesson_number": r[5],
            "lesson_title": r[6],
            "status": r[7],
            "date_added": r[8],
            "progress": r[9]
        }
        for r in rows
    ]

@app.post("/sync")
def sync_videos():
    import glob
    rows = get_all_videos()
    changes = []
    edited_folder = "/home/davidowoh/SelfCraft Media/Edited Videos"

    for r in rows:
        video_id = r[0]
        raw_path = r[1]
        status = r[7]

        # Raw file gone — remove from database
        if not os.path.exists(raw_path):
            delete_video(video_id)
            changes.append(f"Removed missing raw: {raw_path}")
            continue

        # Raw exists — check if output exists
        base = os.path.splitext(os.path.basename(raw_path))[0]
        pattern = os.path.join(edited_folder, f"{base} (Edited*).mp4")
        existing = glob.glob(pattern)

        if existing and status != 'completed':
            update_status(video_id, 'completed')
            update_progress(video_id, None)
            changes.append(f"Marked completed (output exists): {raw_path}")
        elif not existing and status == 'completed':
            update_status(video_id, 'detected')
            update_progress(video_id, None)
            changes.append(f"Reverted to detected (output deleted): {raw_path}")

    return {"synced": True, "changes": changes}

@app.post("/process/{video_id}")
def trigger_process(video_id: int):
    video = get_video_by_id(video_id)
    if not video:
        return {"error": "Video not found"}
    if not os.path.exists(video[1]):
        update_status(video_id, "failed")
        update_progress(video_id, "Source file not found on disk.")
        return {"error": f"File not found on disk: {video[1]}"}
    update_status(video_id, "processing")
    update_progress(video_id, "Starting…")
    try:
        output = process_video(video[1], video_id=video_id)
        update_status(video_id, "completed")
        update_progress(video_id, None)
        return {"status": "completed", "output": output}
    except Exception as e:
        update_status(video_id, "failed")
        update_progress(video_id, f"Error: {str(e)}")
        print(f"Processing failed for video {video_id}: {str(e)}")
        return {"status": "failed", "error": str(e)}

@app.delete("/videos/completed")
def clear_completed():
    delete_completed()
    return {"status": "cleared"}

@app.get("/next-version/{video_id}")
def next_version(video_id: int):
    from app.export.naming import get_next_version_label
    video = get_video_by_id(video_id)
    if not video:
        return {"label": "will create (Edited).mp4"}
    label = get_next_version_label(
        video[1],
        "/home/davidowoh/SelfCraft Media/Edited Videos"
    )
    return {"label": label}