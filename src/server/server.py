from flask import Flask, jsonify, Response, abort
from flask_cors import CORS
import requests
import threading
import time
import os
from xml.etree import ElementTree as ET
import re
import room_hadler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

room_status = {}

DOCKER_CONTAINER_URL = os.getenv("MOCK_URL", "http://localhost:5001")

roomHandler = room_hadler.RoomHandler("config/roomslist.csv")

# Preloading schemes of campus and buildings
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

# Extract mtg names from SVG content
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
            # Здесь можно добавить логику получения реального статуса комнаты
            currentLoad = 10
            maxLoad = roomHandler.get_max_users(scheme_id, roomName)
            roomArray.append({"id": roomName, 
                              "name": roomName, 
                              "count": currentLoad, 
                              "maxCount": maxLoad, 
                              "percentLoad": currentLoad / maxLoad * 100
            })

        return jsonify(roomArray)

    return jsonify({"error": "Invalid scheme id"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)