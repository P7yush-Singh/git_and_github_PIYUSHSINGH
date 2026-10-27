import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")

def landing():
    return "Thanks to DevOps course that help me teach Python Flask"

@app.route("/api", methods=["GET"])

def get_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)