FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY api_gateway.py .
COPY people_counter.py .

RUN mkdir -p /app/images /app/results

EXPOSE 32000

CMD ["sh", "-c", "python3 api_gateway.py & python3 people_counter.py"]
