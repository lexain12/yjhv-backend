from flask import Flask, jsonify, Response, abort
from flask_cors import CORS
import requests
import threading
import time
import os
from xml.etree import ElementTree as ET
import re
from bs4 import BeautifulSoup
from datetime import datetime
import room_hadler as rh

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

room_status = {}

DOCKER_CONTAINER_URL = os.getenv("MOCK_URL", "http://localhost:5001")

roomHandler = rh.RoomHandler("config/roomslist.csv")

SCHEME_DIR = "schemes"
SCHEMES = []

def preload_schemes():
    global SCHEMES
    SCHEMES.clear()
    for idx, filename in enumerate(sorted(os.listdir(SCHEME_DIR))):
        if filename.endswith(".svg"):
            with open(os.path.join(SCHEME_DIR, filename), "r", encoding="utf-8") as f:
                svg_content = f.read()
            SCHEMES.append({"id": idx, "name": filename, "content": svg_content})

preload_schemes()

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

def get_schema_schedule(schema_id):
    with open("schedules/" + str(schema_id) + ".html", 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    schedule = []
    rows = soup.find_all('tr')
    current_day = None

    for row in rows:
        day_img = row.find('img')
        if day_img:
            current_day = day_img['src'].split('/')[-1].split('.')[0]

        cells = row.find_all('td')    
        for cell in cells:
            auditory_tag = cell.find('nobr')
            if auditory_tag:
                time_range = cell.find_previous('td', class_='tdtime').text.strip().replace('<br />', '-')
                subject = cell.text.strip()
                
        

                schedule.append({
                    'day': current_day,
                    'time_range': time_range,
                    'subject': subject,
                    'auditory': auditory_tag.text.strip()
                })
    return schedule

@app.route("/schemes", methods=["GET"])
def get_schemes():
    return jsonify([{"id": s["id"], "name": s["name"]} for s in SCHEMES])

@app.route("/scheme/<int:scheme_id>", methods=["GET"])
def get_scheme_file(scheme_id):
    if 0 <= scheme_id < len(SCHEMES):
        return Response(SCHEMES[scheme_id]["content"], mimetype='image/svg+xml')
    abort(404, description="Scheme not found")

@app.route("/schedule/<int:course_id>", methods=["GET"])
def get_schedule(course_id):
    schedule = get_schema_schedule(course_id)

    if 0 <= course_id <= 5:
        result = []

        for entry in schedule:
            raw = entry['time_range']
            day_str = entry['day']

            cleaned = raw.replace('\u00a0', ' ')
            parts = [p.strip() for p in cleaned.split('-') if ':' in p]

            if len(parts) != 2:
                continue

            start_str, end_str = parts
            start_time = datetime.strptime(start_str, "%H:%M").time()
            end_time = datetime.strptime(end_str, "%H:%M").time()

            now = datetime.now()
            current_time = now.time()
            current_weekday = now.weekday() + 1  # Monday=1, Sunday=7

            day_index = int(day_str.replace("day", ""))

            # Check for the proper day
            same_day = current_weekday == day_index
            in_time_range = start_time <= current_time <= end_time
            is_active = same_day and in_time_range
            

            patched_room_name = "ff-" + entry['auditory']
            patched_room_name.replace("Ц", "c", 1)
            result.append({"auditory": patched_room_name, "time_diff": str(start_time) + " " + str(end_time) + " " + str(current_weekday), "is_active": is_active})

        return jsonify(result)
    
    abort(404, description="Scheme not found")

@app.route("/rooms/<int:scheme_id>", methods=["GET"])
def get_room_info(scheme_id):
    if 0 <= scheme_id < len(SCHEMES):
        extracted_names = extract_mtg_names(SCHEMES[scheme_id]["content"])
        print(extracted_names)
        roomsOnSchemeArray = []
        for roomName in extracted_names:
            currentRoomLoad = 0
            try:
                response = requests.get(f"http://people_counter:32000/count/{roomName}")
                if response.status_code == 200:
                    currentRoomLoad = response.json().get("count", 0)
                else:
                    currentRoomLoad = -1
                    print(f"[WARN] Не удалось получить count для {roomName}: {response}")
            except Exception as e:
                print(f"[ERROR] Ошибка при запросе к сервису count для {roomName}: {e}")
                currentRoomLoad = 0
            maxLoad = roomHandler.get_max_users(scheme_id, roomName)
            roomsOnSchemeArray.append({
                "id": roomName, 
                "room_id": roomName,
                "room_name": roomHandler.get_room_label(scheme_id, roomName),
                "category_id": roomHandler.get_room_category_id(scheme_id, roomName),
                "category_name": roomHandler.get_room_category_label(scheme_id, roomName),
                "count": currentRoomLoad, 
                "maxCount": maxLoad, 
                "percentLoad": f"{currentRoomLoad / maxLoad}"
            })

        return jsonify(roomsOnSchemeArray)

    return jsonify({"error": "Invalid scheme id"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)