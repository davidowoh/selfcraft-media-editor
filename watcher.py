import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database.db import init_db, add_video
from app.media.metadata import extract_metadata

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith(('.mp4', '.mov')):
            print(f"New video detected: {event.src_path}")
            metadata = extract_metadata(event.src_path)
            add_video(event.src_path, metadata)
            print(f"Saved to database: {metadata}")

def watch_folder(path):
    init_db()
    observer = Observer()
    observer.schedule(VideoHandler(), path, recursive=True)
    observer.start()
    print(f"Watching: {path}")
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_folder("/home/davidowoh/SelfCraft Media/Raw Videos")