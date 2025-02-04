# Astrological Horoscope Prediction System 🔮

A machine learning pipeline that generates daily horoscopes by combining astrological data (planetary positions, aspects, lunar phases) with scraped horoscope texts, designed for fine-tuning large language models (LLMs).

## Features 🌟
- **Web Scraping**: Collects historical horoscope data from astrology websites
- **Astrological Data Integration**: Calculates planetary positions, lunar phases, and aspects using Swiss Ephemeris
- **Dataset Preparation**: Creates structured training data for LLM fine-tuning
- **Model Training**: Ready-to-use format for fine-tuning language models

## Installation 🛠️

### Requirements
- Python 3.9+
- [Swiss Ephemeris Files](https://www.astro.com/ftp/swisseph/ephe/) (Download and extract to `./ephe`)

```bash
pip install -r requirements.txt
```

## Usage 🚀

1. Scrape Horoscope Data

```bash
python scrape_horoscopes.py
```

2. Generate Input and Create Dataset for Finetuning

```bash
python main.py
```

## Dataset Structure

```json
{
  "prompt": "Date: 2023-10-25 | Zodiac: Leo | Sun: Scorpio | Moon: Cancer...",
  "completion": "Today brings opportunities for creative expression..."
}
```