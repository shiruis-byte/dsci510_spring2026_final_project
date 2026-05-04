from load import get_top10_states
import pandas as pd
from scipy import stats


def process_unemployment_records(records):
    top10_states = get_top10_states(records)

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
    df = df.sort_values("date")
    df = df[df["state"].isin(top10_states)]

    return df, top10_states


def build_merged_df(unemployment_records, functional_records, recreational_records, top10_states):
    unemp_df = pd.DataFrame(unemployment_records)
    unemp_df["date"] = pd.to_datetime(unemp_df[["year", "month"]].assign(day=1))
    unemp_df = unemp_df[unemp_df["state"].isin(top10_states)]

    func_df = pd.DataFrame(functional_records)
    func_df["date"] = pd.to_datetime(func_df[["year", "month"]].assign(day=1))
    func_avg = func_df.groupby(["state", "date"])["search_index"].mean().reset_index()
    func_avg.rename(columns={"search_index": "functional_avg"}, inplace=True)

    rec_df = pd.DataFrame(recreational_records)
    rec_df["date"] = pd.to_datetime(rec_df[["year", "month"]].assign(day=1))
    rec_avg = rec_df.groupby(["state", "date"])["search_index"].mean().reset_index()
    rec_avg.rename(columns={"search_index": "recreational_avg"}, inplace=True)

    merged = unemp_df.merge(func_avg, on=["state", "date"], how="inner")
    merged = merged.merge(rec_avg, on=["state", "date"], how="inner")

    return merged

# AI(Claude) generated: Pearson correlation calculation using scipy
def run_correlation_analysis(merged_df):
    print("\nPearson Correlation Analysis")
    results = []

    for state in merged_df["state"].unique():
        state_df = merged_df[merged_df["state"] == state].dropna()

        func_corr, func_p = stats.pearsonr(state_df["unemployment_rate"], state_df["functional_avg"])
        rec_corr, rec_p = stats.pearsonr(state_df["unemployment_rate"], state_df["recreational_avg"])

        results.append({
            "state": state,
            "func_corr": round(func_corr, 3),
            "func_pvalue": round(func_p, 4),
            "rec_corr": round(rec_corr, 3),
            "rec_pvalue": round(rec_p, 4)
        })

        sig_func = "significant" if func_p < 0.05 else "not significant"
        sig_rec = "significant" if rec_p < 0.05 else "not significant"
        print(f"  {state}: Functional r={func_corr:.3f} ({sig_func}), Recreational r={rec_corr:.3f} ({sig_rec})")

    corr_df = pd.DataFrame(results)
    print(f"\nAvg Functional correlation: r={corr_df['func_corr'].mean():.3f}")
    print(f"Avg Recreational correlation: r={corr_df['rec_corr'].mean():.3f}")

    return corr_df