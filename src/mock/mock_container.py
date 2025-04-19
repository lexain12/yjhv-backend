from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/<roomName>', methods=['GET'])
def room_data(roomName: str):
    data = {
        "room_id": "101",
        "occupancy": 10
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
