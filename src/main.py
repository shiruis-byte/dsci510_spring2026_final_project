import os
from config import BLS_API_KEY, BLS_START_YEAR, BLS_END_YEAR, DATA_DIR, RESULTS_DIR
from load import get_unemployment_data
from process import process_unemployment_records
from analyze import run_analysis

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("=== Fetching BLS unemployment data ===")
    records = get_unemployment_data(BLS_API_KEY, BLS_START_YEAR, BLS_END_YEAR)
    print(f"Fetched {len(records)} records total.\n")

    print("=== Processing: finding top 10 states ===")
    df, top10_states = process_unemployment_records(records)
    print()

    print("=== Analyzing: generating plots ===")
    run_analysis(records, top10_states, RESULTS_DIR)

    print("\n=== Done! Check the results/ folder for plots. ===")
