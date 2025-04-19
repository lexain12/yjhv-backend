from flask import Flask, jsonify
import requests
import threading
import time
import os

app = Flask(__name__)

room_status = {}

DOCKER_CONTAINER_URL = os.getenv("MOCK_URL", "http://localhost:5001/room_data")

def update_room_status():
    while True:
        try:
            response = requests.get(DOCKER_CONTAINER_URL, timeout=5)
            if response.status_code == 200:
                room_status.update(response.json())
            else:
                print("Ошибка при получении данных:", response.status_code)
        except Exception as e:
            print("Ошибка подключения к контейнеру:", e)
        time.sleep(5)  # каждые 60 секунд

@app.route('/room_status', methods=['GET'])
def get_room_status():
    return jsonify(room_status)

if __name__ == '__main__':
    threading.Thread(target=update_room_status, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
