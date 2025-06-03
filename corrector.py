from openai import OpenAI
from config import OPENAI_API_KEY
 
client = OpenAI(api_key=OPENAI_API_KEY)
 
def correct_message(message):
    prompt = (
        "Please review and correct the following FWB/16 message:\n"
        "- Remove invalid characters (e.g., #, $, %, repeated letters).\n"
        "- DO NOT truncate or delete valid reference numbers or IDs.\n"
        "- Preserve valid numeric values, including long reference numbers.\n"
        "- DO NOT remove slashes or field delimiters.\n"
        "- Remove extra blank lines if present.\n"
        "- Preserve correct formatting, line spacing, and structure as per Cargo-IMP FWB/16 guidelines.\n"
        "\nHere is the message:\n{msg}"
        ).format(msg=message)
 
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in IATA Cargo-IMP FWB/16 message standards. You correct format and character issues while preserving all valid data and structure."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1000
    )
 
    return response.choices[0].message.content.strip()
