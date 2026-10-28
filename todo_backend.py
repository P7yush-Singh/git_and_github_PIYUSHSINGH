import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Configure your MongoDB connection first."
    )

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["git_github_assignment"]
todo_collection = db["todo_items"]


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName", "").strip()
    item_description = request.form.get("itemDescription", "").strip()

    if request.is_json:
        data = request.get_json(silent=True) or {}
        item_name = str(data.get("itemName", "")).strip()
        item_description = str(data.get("itemDescription", "")).strip()

    if not item_name or not item_description:
        return jsonify({
            "success": False,
            "message": "Item Name and Item Description are required."
        }), 400

    try:
        result = todo_collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

        return jsonify({
            "success": True,
            "message": "To-Do item saved successfully.",
            "itemId": str(result.inserted_id)
        }), 201

    except PyMongoError:
        app.logger.exception("Failed to save To-Do item")
        return jsonify({
            "success": False,
            "message": "Could not save the To-Do item."
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)