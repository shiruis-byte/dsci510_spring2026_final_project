# Economic Stress and Social Media Seeking (2019–2024)
**Author:** Shirui Sun

> **AI Disclosure:** Claude (Anthropic) was used to assist with coding in this project. Specifically, the random time delay logic for Google Trends requests and the Pearson correlation analysis are AI-generated. All AI-generated code sections are labeled with `# AI generated:` comments in the source files.

## Introduction

This project examines how the economic shock influenced individuals' behavioral preferences on social media from 2019 to 2024, specifically whether people tend to shift toward job-seeking (functional usage) or entertainment (recreational usage) under rising unemployment. The analysis focuses on three research questions: how unemployment trends changed before, during, and after COVID-19; whether higher unemployment leads to increased functional social media usage; and whether higher unemployment leads to increased recreational social media usage. 

To answer these questions, monthly unemployment data for all 50 states was retrieved from the BLS API, and the top 10 highest-unemployment states were identified. Google Trends search interest data was then collected via pytrends for both functional keywords (LinkedIn, Job, Hiring) and recreational keywords (TikTok, Netflix, Instagram) across these 10 states. The two datasets were merged and Pearson correlation analysis was performed to measure the relationship between unemployment rate and each type of social media behavior. The analytical focus is on unemployment trends across the 10 highest-unemployment states and the comparison between functional and recreational social media responses to economic stress.

In this project, the full analysis can be run end-to-end using `main.py`, or interactively via `results.ipynb`. `tests.py` is provided to verify the functions and does not reproduce the complete results.

# Data sources
| # | Name | Source | Type | Fields | Data Points (Final Use) |
|---|------|--------|------|--------|-------------------------|
| 1 | Bureau of Labor Statistics (BLS) | https://api.bls.gov/publicAPI/v2/timeseries/data/ | API | state, year, month, unemployment_rate | 3600                    |
| 2 | Google Trends – Functional (LinkedIn, Job, Hiring) | https://trends.google.com | API (pytrends) | state, month, search_interest_index | 2160                    |
| 3 | Google Trends – Recreational (TikTok, Netflix, Instagram) | https://trends.google.com | API (pytrends) | state, month, search_interest_index | 2160                    |
**Notes:**
- **Functional social media behavior**: the job-seeking social media behavior, measured by search interest in keywords: "LinkedIn", "Job", and "Hiring".
- **Recreational social media behavior**: the entertainment social media behavior, measured by search interest in keywords: "TikTok", "Netflix", and "Instagram".
- **Search interest index**: a relative measure (0–100) of how popular a keyword is over time. It does NOT represent actual search counts.
- **pytrends**: an unofficial Python library for accessing Google Trends data. Google may temporarily block requests (Error 429), which is handled by adding random time delays between requests.

# Results

Overall, both types of social media behavior are clearly related to unemployment, but they respond differently. 

From the time patterns, job-seeking behavior shows a delayed response, while entertainment behavior responds immediately during the unemployment spike. 

From the correlation results, higher unemployment leads to more recreational media behavior, with a moderate positive correlation (r = 0.661) that is statistically significant. At the same time, higher unemployment is associated with lower job-seeking activity, with a weaker negative correlation of r = -0.400, which is also statistically significant.

These results suggest that under economic stress, people tend to turn to entertainment first as a short-term coping strategy, and only later increase job-seeking behavior.

# Installation
- Set your BLS API key as an environment variable before running the project:
  - Mac/Linux: `export BLS_API_KEY=your_key_here`
  - Windows: `set BLS_API_KEY=your_key_here`
- Register for a free BLS API key at: https://data.bls.gov/registrationEngine/
- No API key is needed for Google Trends (pytrends)
- Required packages: `pip install -r requirements.txt`
  - requests, pandas, matplotlib, pytrends, scipy

# Running analysis

From `src/` directory run:

`python main.py`

Results will appear in `results/` folder.

To run the Jupyter notebook from the project root directory:

`jupyter notebook results.ipynb`

To run tests from `src/` directory:

`python tests.py`
