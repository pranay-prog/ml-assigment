import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutoPusher(FileSystemEventHandler):
    def __init__(self, debounce_seconds=10):
        self.debounce_seconds = debounce_seconds
        self.last_run = 0

    def on_any_event(self, event):
        if ".git" in event.src_path:
            return

        now = time.time()
        if now - self.last_run < self.debounce_seconds:
            return

        self.last_run = now

        print("\n[AutoPush] Detected change, checking git status...")

        status = os.popen("git status --porcelain").read().strip()
        if status == "":
            print("[AutoPush] Nothing to commit.")
            return

        os.system("git add .")
        os.system('git commit -m "Auto update"')
        os.system("git push")

        print("[AutoPush] Done.")

if __name__ == "__main__":
    path = "."
    event_handler = GitAutoPusher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("🚀 Auto push is running. Save a file to test it. Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[AutoPush] Stopping...")
        observer.stop()
    observer.join()
