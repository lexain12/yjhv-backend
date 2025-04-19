from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/room_data', methods=['GET'])
def room_data():
    data = {
        "room_id": "101",
        "occupancy": random.randint(0, 10)
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
