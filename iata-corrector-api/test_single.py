from dotenv import load_dotenv
load_dotenv()

from corrector import correct_message

sample_msg = """FHL/5
888-54656630MEXACA/T1K10.0
HBS/HAWB1/MEXACA/1/K10.0//TOYS
TXT/TOYS
"""

if __name__ == "__main__":
    try:
        corrected = correct_message(sample_msg)
        print("Original Message:\n", sample_msg)
        print("\nCorrected Message:\n", corrected)
    except Exception as e:
        print("Error connecting to OpenAI:", e)
        print("Fallback: Please check your internet connection or proxy settings.")
