import pandas as pd
from corrector import correct_ffr6_message

def evaluate_corrections(validation_path):
    df = pd.read_csv(validation_path)
    df['Corrected'] = df['MSG_TXT'].apply(correct_ffr6_message)
    df['Match'] = df['Corrected'].str.strip() == df['EDIT_MSG'].str.strip()
    return df
