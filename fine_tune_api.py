import os
from flask import Blueprint, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

fine_tune_api = Blueprint("fine_tune_api", __name__)
client = OpenAI(api_key=api_key)

@fine_tune_api.route("/api/train-model", methods=["POST"])
def train_model():
    try:
        training_path = "static/data/fwb_training_data.jsonl"

        # Upload the file
        uploaded_file = client.files.create(
            file=open(training_path, "rb"),
            purpose="fine-tune"
        )

        # Start fine-tuning job
        fine_tune_job = client.fine_tuning.jobs.create(
            training_file=uploaded_file.id,
            model="gpt-3.5-turbo"
        )

        return jsonify({"status": "started", "job_id": fine_tune_job.id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
