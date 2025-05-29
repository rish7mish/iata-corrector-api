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

    prompt = """Please correct the following IATA FWB/16 cargo message by ensuring proper format, accurate line breaks, and removing any unnecessary whitespace or punctuation while preserving the meaning and content. While responding please provide only the corrected message without any extra context.

Examples:

Original message:
"FWB/17\\n117-41380802ARNEWR/T3K268.8MC2.93\\nSHP\\nNAM/DACHSER FINLANDAIR . SEA LOGISTICSO\\n/Y\\nADR/AEYRITIE 8 B\\nLOC/VANTAA\\n/FI/01510/TE/3589825561\\nCNE\\nNAM/DACHSER USAAIR . SEA LOGISTICS INC.\\nADR/90 MERRICK AVENUE. SUITE 505\\nLOC/EAST MEADOW/NY\\n/US/11554/TE/15165617800\\nAGT//1947090/0153\\n/DACHSER FINLAND\\n/HELSINKI\\nSSR/E FREIGHT SHPT WITH ACCOMPANYING DOCS\\nACC/GEN/GENERAL CARGO\\nCVD/EUR/PP/PP/NVD/NCV/XXX\\nRTD/1/P3/K268.8/CQ/W488/R3.99/T1947.12\\n/NG/CONSOLIDATED CA\\n/2/NG/S PER ATTACHED MANIF\\n/3/NG/EST\\n/4/NH/39172900\\n/5/NH/39173200\\n/6/ND//CMT34-34-25/1\\n/7/ND//CMT163-87-100/1\\n/8/ND//CMT120-80-154/1\\n/9/NV/MC2.93\\nPPD/WT1947.12\\n/CT1947.12\\nCER/KAUNISVESI\\nISU/22MAY25/VANTAA/DACHSER FINLAND AIR\\nOSI/HAWB.S ENCLOSED TO CONSOLIDATION POUCH\\nREF/CDGHQXH\\nCOR/X\\nSPH/ECC/EAP/SPX/NST\\nOCI/US/CNE/T/TAX NO.13-2793095\\n/FI/ISS/RA/00207-01\\n///ED/0128\\n/FI/OSS/RA/00118-01\\n///SM/XRY\\n///SN/KAUNISVESI KIIA\\n///SD/22MAY251342\\n/FI/EXP/M/25FIV00000477982B2\\n/FI/EXP/M/25FIV00000495247B5\\n/FI/OSS/RA/00102-01"

Corrected message:
"FWB/17\\n117-41380802ARNEWR/T3K268.8MC2.93\\nRTG/ARNSK/EWRSK\\nSHP\\nNAM/DACHSER FINLANDAIR . SEA LOGISTICSO\\n/Y\\nADR/AEYRITIE 8 B\\nLOC/VANTAA\\n/FI/01510/TE/3589825561\\nCNE\\nNAM/DACHSER USAAIR . SEA LOGISTICS INC.\\nADR/90 MERRICK AVENUE. SUITE 505\\nLOC/EAST MEADOW/NY\\n/US/11554/TE/15165617800\\nAGT//1947090/0153\\n/DACHSER FINLAND\\n/HELSINKI\\nSSR/E FREIGHT SHPT WITH ACCOMPANYING DOCS\\nACC/GEN/GENERAL CARGO\\nCVD/EUR/PP/PP/NVD/NCV/XXX\\nRTD/1/P3/K268.8/CQ/W488/R3.99/T1947.12\\n/NG/CONSOLIDATED CA\\n/2/NG/S PER ATTACHED MANIF\\n/3/NG/EST\\n/4/NH/39172900\\n/5/NH/39173200\\n/6/ND//CMT34-34-25/1\\n/7/ND//CMT163-87-100/1\\n/8/ND//CMT120-80-154/1\\n/9/NV/MC2.93\\nPPD/WT1947.12\\n/CT1947.12\\nCER/KAUNISVESI\\nISU/22MAY25/VANTAA/DACHSER FINLAND AIR\\nOSI/HAWB.S ENCLOSED TO CONSOLIDATION POUCH\\nREF/CDGHQXH\\nCOR/X\\nSPH/ECC/EAP/SPX/NST\\nOCI/US/CNE/T/TAX NO.13-2793095\\n/FI/ISS/RA/00207-01\\n///ED/0128\\n/FI/OSS/RA/00118-01\\n///SM/XRY\\n///SN/KAUNISVESI KIIA\\n///SD/22MAY251342\\n/FI/EXP/M/25FIV00000477982B2\\n/FI/EXP/M/25FIV00000495247B5\\n/FI/OSS/RA/00102-01"

...
"""

    
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
