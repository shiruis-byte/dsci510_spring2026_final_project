import os
from config import BLS_START_YEAR, BLS_END_YEAR, DATA_DIR, RESULTS_DIR
from load import get_unemployment_data, get_functional_trends, get_recreational_trends
from process import process_unemployment_records, build_merged_df, run_correlation_analysis
from analyze import run_analysis

if __name__ == "__main__":
    BLS_API_KEY = os.getenv("BLS_API_KEY")
    if not BLS_API_KEY:
        raise EnvironmentError("BLS_API_KEY not set. Run: export BLS_API_KEY=your_key")

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Step 1: get unemployment data from BLS API
    print("Step 1: Fetching BLS unemployment data...")
    records = get_unemployment_data(BLS_API_KEY, BLS_START_YEAR, BLS_END_YEAR)
    print(f"Fetched {len(records)} records total.")

    # Step 2: find top 10 states with the highest unemployment rate
    print("\nStep 2: Finding top 10 states...")
    df, top10_states = process_unemployment_records(records)

    # Step 3: get Google Trends data for functional and recreational keywords
    functional_records = get_functional_trends(top10_states)
    print(f"Fetched {len(functional_records)} functional trend records.")

    recreational_records = get_recreational_trends(top10_states)
    print(f"Fetched {len(recreational_records)} recreational trend records.")

    # Step 4: run Pearson correlation analysis
    print("\nStep 4: Running correlation analysis...")
    merged_df = build_merged_df(records, functional_records, recreational_records, top10_states)
    corr_df = run_correlation_analysis(merged_df)

    # Step 5: generate all plots
    print("\nStep 5: Generating plots...")
    run_analysis(records, top10_states, functional_records, recreational_records, RESULTS_DIR)

    print("\nDone! Check the results/ folder for plots.")