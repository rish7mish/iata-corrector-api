import json
import os
from flask import Blueprint, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
os.makedirs('config', exist_ok=True)
api_key = os.getenv("OPENAI_API_KEY")

fine_tune_api = Blueprint("fine_tune_api", __name__)
client = OpenAI(api_key=api_key)

@fine_tune_api.route("/api/train-model", methods=["POST"])
def train_model():
    try:
        training_path = "static/data/fwb_training_data.jsonl"

        uploaded_file = client.files.create(
            file=open(training_path, "rb"),
            purpose="fine-tune"
        )

        fine_tune_job = client.fine_tuning.jobs.create(
            training_file=uploaded_file.id,
            model="gpt-3.5-turbo"
        )

        return jsonify({"status": "started", "job_id": fine_tune_job.id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@fine_tune_api.route("/api/train-status/<job_id>", methods=["GET"])
def check_fine_tune_status(job_id):
    try:
        job = client.fine_tuning.jobs.retrieve(job_id)

        # Save model ID only if training succeeded
        if job.status == "succeeded" and job.fine_tuned_model:
            with open("config/fine_tuned_model.json", "w") as f:
                json.dump({"model_id": job.fine_tuned_model}, f)

        return jsonify({
            "status": job.status,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "fine_tuned_model": job.fine_tuned_model
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
