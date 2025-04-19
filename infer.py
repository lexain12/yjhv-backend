import os
from pathlib import Path
from ultralytics import YOLO
import cv2

model = YOLO("yolov8m.pt")

dir_path = Path("./test_images")
paths = sorted(os.listdir(dir_path))
for img_path in paths:
    image = cv2.imread(dir_path / img_path)

    # Детекция
    results = model(image, imgsz=1280, conf=0.1, iou=0.8, agnostic_nms=True)[0]

    # Подсчет людей
    person_count = 0
    for box in results.boxes:
        cls_id = int(box.cls[0].item())
        conf = box.conf[0].item()
        if cls_id == 0 and conf > 0.4:  # Класс 0 — человек
            person_count += 1
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            cv2.rectangle(image, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)

    # Надпись
    cv2.putText(image, f"People: {person_count}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imwrite(f"./results/{img_path}", image)
