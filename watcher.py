import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith(('.mp4', '.mov')):
            print(f"New video detected: {event.src_path}")

def watch_folder(path):
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