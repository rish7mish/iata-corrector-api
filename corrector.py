import json
from openai import OpenAI
from config import OPENAI_API_KEY
 
client = OpenAI(api_key=OPENAI_API_KEY)
 
def detect_message_type(message):
    for line in message.splitlines():
        if line.strip().startswith(("FFR/6", "FHL/5", "FWB/16")):
            return line.strip().split()[0]
    return "FFR/6"  # default fallback
 
def correct_message(message):
    message_type = detect_message_type(message)
 
    prompt = (
        "You are an expert in IATA Cargo-IMP messaging standards. Please review and correct the following {msg_type} message.\n"
        "Remove any extra characters or invalid strings and extra blank lines that do not conform to the standard, such as repeated letters, overly long reference codes, or placeholder text.\n"
        "Do not delete valid fields.\n"
        "Remove extra blank lines if present.\n"
        "Preserve correct formatting, spacing, line structure as per Cargo-IMP guidelines.\n"
        "Here is the message:\n\n{msg}"
    ).format(msg_type=message_type, msg=message)
 
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
