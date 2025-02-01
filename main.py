import pandas as pd
from astro_utils import get_planetary_positions, get_lunar_phase, get_aspects
from datetime import datetime, timedelta



def create_prompt(row):
    date = datetime.strptime(row['Date'], '%Y-%m-%d')
    positions = get_planetary_positions(date)
    lunar_phase = get_lunar_phase(date)
    aspects = get_aspects(date)
    
    prompt = (
        f"Date: {row['Date']} | Zodiac: {row['Zodiac Sign']} | "
        f"Sun: {positions['Sun']} | Moon: {positions['Moon']} | "
        f"Mercury: {positions['Mercury']} | Venus: {positions['Venus']} | "
        f"Mars: {positions['Mars']} | Jupiter: {positions['Jupiter']} | "
        f"Saturn: {positions['Saturn']} | Uranus: {positions['Uranus']} | "
        f"Neptune: {positions['Neptune']} | Pluto: {positions['Pluto']} | "
        f"Lunar Phase: {lunar_phase} | Aspects: {', '.join(aspects)}"
    )
    return prompt
    

if __name__ == "__main__":
# Load your scraped horoscope CSV
    df = pd.read_csv('horoscopes.csv')
    df['prompt'] = df.apply(create_prompt, axis=1)
    df['completion'] = df['Horoscope Text']

    # Save to JSONL format for fine-tuning
    df[['prompt', 'completion']].to_json('horoscope_finetune.jsonl', orient='records', lines=True)