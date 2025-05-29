import os
import json
from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
os.makedirs("static/data", exist_ok=True)
os.makedirs("config", exist_ok=True)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

train_all_api = Blueprint("train_all_api", __name__)

@train_all_api.route("/api/train-all", methods=["POST"])
def train_all():
    try:
        # Step 1: Accept JSON training data
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"status": "error", "message": "Payload must be a JSON array."}), 400

        # Step 2: Convert to JSONL
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

        # Step 3: Upload file to OpenAI
        uploaded_file = client.files.create(file=open(jsonl_path, "rb"), purpose="fine-tune")

        # Step 4: Start fine-tune job
        fine_tune_job = client.fine_tuning.jobs.create(
            training_file=uploaded_file.id,
            model="gpt-3.5-turbo"
        )

        # Return job ID
        return jsonify({"status": "started", "job_id": fine_tune_job.id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})