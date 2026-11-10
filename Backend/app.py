import os

from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://<user>:<password>@peter.yzwqobh.mongodb.net/?retryWrites=true&w=majority",
)

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["todo_db"]
collection = db["todo_items"]


@app.route("/")
def home():
    return "Backend is running"


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400

    try:
        collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description,
        })
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return jsonify({"message": "To-Do item saved"}), 201


if __name__ == "__main__":
    app.run(debug=True)