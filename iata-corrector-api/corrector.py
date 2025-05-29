import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def detect_message_type(message):
    for line in message.splitlines():
        if line.strip().startswith(("FFR/6", "FHL/5", "FWB/16")):
            return line.strip().split()[0]
    return "FFR/6"

def correct_message(message, prompts_file="prompts.json"):
    with open(prompts_file, "r") as f:
        prompt_templates = json.load(f)

    message_type = detect_message_type(message)
    prompt = prompt_templates.get(message_type, prompt_templates["FFR/6"]).replace("{msg}", message)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are an expert in {message_type} format."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()
