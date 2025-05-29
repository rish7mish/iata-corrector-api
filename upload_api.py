import os
import json
from flask import Blueprint, request, jsonify

upload_api = Blueprint("upload_api", __name__)
os.makedirs("static/data", exist_ok=True)

@upload_api.route("/api/upload-training-data", methods=["POST"])
def upload_training_data():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"status": "error", "message": "Payload must be a JSON array."}), 400

        jsonl_path = "static/data/fwb_training_data.jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for item in data:
                record = {
                    "messages": [
                        {"role": "system", "content": "You are a validator and corrector of IATA FWB/16 messages. Fix only the necessary segments based on the provided error."},
                        {"role": "user", "content": f"Error: {item['error_msg']}\nMessage:\n{item['msg_txt']}"},
                        {"role": "assistant", "content": item['edit_msg']}
                    ]
                }
                f.write(json.dumps(record) + "\n")

        return jsonify({"status": "success", "file": jsonl_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})