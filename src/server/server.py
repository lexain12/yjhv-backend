from flask import Flask, jsonify, Response, abort
import requests
import threading
import time
import os
from xml.etree import ElementTree as ET
import re

app = Flask(__name__)

room_status = {}

DOCKER_CONTAINER_URL = os.getenv("MOCK_URL", "http://localhost:5001")

# preloading schemes of campus and buildings
SCHEME_DIR = "schemes"
SCHEMES = []

# Preload SVG files into memory
def preload_schemes():
    global SCHEMES
    SCHEMES.clear()
    for idx, filename in enumerate(sorted(os.listdir(SCHEME_DIR))):
        if filename.endswith(".svg"):
            with open(os.path.join(SCHEME_DIR, filename), "r", encoding="utf-8") as f:
                svg_content = f.read()
            SCHEMES.append({"id": idx, "name": filename, "content": svg_content})

preload_schemes()

# Goes to docker container of our ML team and get current info about room
def update_room_status(name: str):
    while True:
        try:
            roomUrl = DOCKER_CONTAINER_URL + "/" + name
            response = requests.get(roomUrl, timeout=5)
            if response.status_code == 200:
                return Response.json()
            else:
                print("Ошибка при получении данных:", response.status_code)
        except Exception as e:
            print("Ошибка подключения к контейнеру:", e)
        time.sleep(5)  # каждые 60 секунд

# 
def extract_mtg_names(svg_content: str) -> list[str]:
    tree = ET.fromstring(svg_content)
    mtg_names = []

    for elem in tree.iter():
        elem_id = elem.attrib.get("id")
        if elem_id:
            match = re.fullmatch(r"mtg-(.*?)-mtg", elem_id)
            if match:
                mtg_names.append(match.group(1))
    
    return mtg_names

@app.route("/schemes", methods=["GET"])
def get_schemes():
    return jsonify([{"id": s["id"], "name": s["name"]} for s in SCHEMES])

@app.route("/scheme/<int:scheme_id>", methods=["GET"])
def get_scheme_file(scheme_id):
    if 0 <= scheme_id < len(SCHEMES):
        return Response(SCHEMES[scheme_id]["content"], mimetype='image/svg+xml')
    abort(404, description="Scheme not found")


@app.route("/rooms/<int:scheme_id>", methods=["GET"])
def get_room_info(scheme_id):
    if 0 <= scheme_id < len(SCHEMES):
        extracted_names = extract_mtg_names(SCHEMES[scheme_id]["content"])
        roomArray = []
        for roomName in extracted_names:
            print(roomName)
            roomArray.append(update_room_status(roomName))

        return jsonify(roomArray)

    return jsonify({"Invalid scheme id"}), 500
    # abort(404, description="Scheme not found")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
