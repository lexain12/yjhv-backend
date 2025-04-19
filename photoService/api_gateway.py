from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'images'
RESULTS_FOLDER = 'results'

@app.route('/upload', methods=['PUT'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.png'):
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"status": "success", "filename": filename}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/count/<room>', methods=['GET'])
def get_count(room):
    result_file = os.path.join(RESULTS_FOLDER, f"{room}.txt")
    if not os.path.exists(result_file):
        return jsonify({"error": "Room not found"}), 404
    
    with open(result_file, 'r') as f:
        count = f.read().strip()
    return jsonify({"room": room, "count": int(count)}), 200

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=32000)
