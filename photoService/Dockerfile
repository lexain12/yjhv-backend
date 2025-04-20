FROM python:3.9-slim


WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python3 -c "from ultralytics import YOLO; YOLO('yolov8m.pt')"

COPY api_gateway.py .
COPY people_counter.py .

RUN mkdir -p /app/images /app/results

EXPOSE 32000

CMD ["sh", "-c", "python3 api_gateway.py & python3 -u people_counter.py"]
