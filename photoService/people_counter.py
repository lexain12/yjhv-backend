import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ultralytics import YOLO
import cv2

# Инициализация модели
model = YOLO("yolov8m.pt")

# Конфигурация путей
WATCH_DIR = Path("./images")
RESULTS_DIR = Path("./results")
RESULTS_DIR.mkdir(exist_ok=True, parents=True)

class ImageHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"Event type: {event.event_type} | Path: {event.src_path}")
    def on_created(self, event):
        if not event.is_directory:
            print("on_create")
            self.process_image(Path(event.src_path))

    def process_image(self, src_path):
        try:
            print(f"processing {src_path}")
            image = cv2.imread(str(src_path))
            if image is None:
                return

            results = model(image, imgsz=1280, conf=0.1, iou=0.8, agnostic_nms=True)[0]
            person_count = sum(1 for box in results.boxes if int(box.cls[0]) == 0 and box.conf[0] > 0.4)

            with open(RESULTS_DIR / f"{src_path}.txt", "a") as f:
                f.write(f"{person_count}\n")

            os.remove(src_path)

        except Exception as e:
            print(f"Error processing {src_path.name}: {e}")

if __name__ == "__main__":
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(WATCH_DIR), recursive=False)
    observer.start()

    try:
        while True:
            print("I am working")
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()