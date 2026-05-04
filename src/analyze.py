import os
from load import plot_unemployment_trends, plot_trends_comparison, plot_average_trends

# This function generates all the plots for the analysis
def run_analysis(records, top10_states, functional_records, recreational_records, results_dir="../results"):
    os.makedirs(results_dir, exist_ok=True)

    plot_unemployment_trends(records, top10_states, result_dir=results_dir)

    # Plot of unemployment vs functional search trends
    if functional_records:
        plot_trends_comparison(records, functional_records, top10_states,
                               category="functional", result_dir=results_dir)

    # Plot of unemployment vs recreational search trends
    if recreational_records:
        plot_trends_comparison(records, recreational_records, top10_states,
                               category="recreational", result_dir=results_dir)

    # Plot of the average trends across all states
    if functional_records and recreational_records:
        plot_average_trends(records, functional_records, recreational_records,
                            top10_states, result_dir=results_dir)

    print(f"All plots saved to {results_dir}/")