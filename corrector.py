import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def detect_message_type(message):
    for line in message.splitlines():
        if line.strip().startswith(("FFR/6", "FHL/5", "FWB/16")):
            return line.strip().split()[0]
    return "FFR/6"

def correct_message(message):
    message_type = detect_message_type(message)

   prompt = (
    "You are an expert in IATA FWB/16 cargo message formats. "
    "Replace two consecutive newline characters with a single newline character. "
    "Remove extra characters from every segment. Preserve all forward slashes. "
    "Correct this message:\n{msg}"
).format(msg=message)


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
