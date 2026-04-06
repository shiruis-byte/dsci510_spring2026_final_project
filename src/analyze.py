import os
from load import plot_unemployment_trends


def run_analysis(records: list, top10_states: list, results_dir: str = "../results") -> None:
    os.makedirs(results_dir, exist_ok=True)
    plot_unemployment_trends(records, top10_states, result_dir=results_dir)
    print(f"Plot saved to {results_dir}/unemployment_trends.png")