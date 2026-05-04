import os

#Paths
DATA_DIR = "../data"
RESULTS_DIR = "../results"

#BLS API
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
BLS_START_YEAR = "2019"
BLS_END_YEAR = "2024"

#Google Trends
TRENDS_TIMEFRAME = "2019-01-01 2024-12-31"
TRENDS_MIN_DELAY = 4.0
TRENDS_MAX_DELAY = 8.0
FUNCTIONAL_KEYWORDS = ["LinkedIn", "Job", "Hiring"]
RECREATIONAL_KEYWORDS = ["TikTok", "Netflix", "Instagram"]