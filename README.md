# 📘 IATA FWB Corrector API – Documentation

A Flask-based API to upload, train, and correct IATA FWB/16 messages using OpenAI fine-tuning.

---

## 🔧 Base URL
- `http://localhost:5000/`
- Or your deployed URL on Render/GitHub Pages/etc.

---

## 📤 POST `/api/upload-training-data`
**Purpose**: Accept raw training data as JSON and convert to OpenAI `.jsonl`.

### 🔸 Request Body
```json
[
  {
    "msg_txt": "FWB/16\n...",
    "error_msg": "Missing SHP segment",
    "edit_msg": "FWB/16\nSHP/..."
  }
]
```

### ✅ Response
```json
{
  "status": "success",
  "file": "static/data/fwb_training_data.jsonl"
}
```

---

## 🚀 POST `/api/train-model`
**Purpose**: Starts a fine-tuning job using the previously uploaded training file.

### ✅ Response
```json
{
  "status": "started",
  "job_id": "ftjob-abc123..."
}
```

---

## 📈 GET `/api/train-status/<job_id>`
**Purpose**: Checks the status of the fine-tuning job and saves the model ID.

### ✅ Response (when training is complete)
```json
{
  "status": "succeeded",
  "fine_tuned_model": "ft:gpt-3.5-turbo-0613:org::xyz456",
  "created_at": 1234567890,
  "updated_at": 1234569999
}
```

---

## 🧠 POST `/api/correct`
**Purpose**: Uses the saved fine-tuned model to correct an IATA message.

### 🔸 Request Body
```json
{
  "msg_txt": "FWB/16\n...",
  "error_msg": "Missing SHP segment"
}
```

### ✅ Response
```json
{
  "corrected_message": "FWB/16\nSHP/..."
}
```

---

## 🎯 POST `/api/train-all`
**Purpose**: Upload + Convert + Train (All in One)

### 🔸 Request Body
Same format as `/api/upload-training-data`.

### ✅ Response
```json
{
  "status": "started",
  "job_id": "ftjob-xyz456..."
}
```

---

## 📌 Notes
- Training file is saved at: `static/data/fwb_training_data.jsonl`
- Fine-tuned model ID is saved at: `config/fine_tuned_model.json`
- Make sure `OPENAI_API_KEY` is set in `.env` or Render environment

---

## 🧪 Test with `curl`

```bash
curl -X POST http://localhost:5000/api/train-all \
  -H "Content-Type: application/json" \
  -d @sample_training.json
```

---

## 📂 File Structure (Key Files)

```
config/fine_tuned_model.json      # Stores model ID
static/data/fwb_training_data.jsonl  # JSONL training file
```

---

## 📞 Contact
For improvements, UI integration, or more formats (Postman, Swagger), contact the developer team.
