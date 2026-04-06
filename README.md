# Economic Stress and Social Media Seeking

**DSCI 510 – Spring 2026 | University of Southern California**  
Shirui Sun 

## Project Summary

This project investigates how economic stress, measured by state-level unemployment rates, influences social media engagement behavior. Social media engagement is categorized into two types:
- **Functional** (career-focused): LinkedIn, Job, Hiring keywords
- **Recreational** (entertainment-focused): TikTok, Netflix, Instagram keywords

The analysis covers the 10 U.S. states with the highest average unemployment rates from 2019 to 2024.

## Data Sources

| # | Name | Source | Type | Fields |
|---|------|--------|------|--------|
| 1 | Bureau of Labor Statistics (BLS) | https://api.bls.gov/publicAPI/v2/timeseries/data/ | API | state, year, month, unemployment_rate |
| 2 | Google Trends – Functional (LinkedIn, Job, Hiring) | https://trends.google.com | API (pytrends) | state, month, search_interest_index |
| 3 | Google Trends – Recreational (TikTok, Netflix, Instagram) | https://trends.google.com | API (pytrends) | state, month, search_interest_index |

## Installation

1. Clone the repository
2. Install required packages:
```
pip install -r requirements.txt
```
3. Create a `.env` file in the `src/` directory based on `.env.example`:
```
BLS_API_KEY=your_bls_api_key_here
```
You can register for a free BLS API key at: https://data.bls.gov/registrationEngine/

## Running the Analysis

From the `src/` directory, run:
```
python main.py
```

Results (plots) will be saved to the `results/` folder.  
Downloaded data will be stored in the `data/` folder.

## Running Tests

From the `src/` directory, run:
```
export BLS_API_KEY=your_key_here   # Mac/Linux
python tests.py
```

