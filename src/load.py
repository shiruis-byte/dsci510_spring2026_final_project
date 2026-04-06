import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_unemployment_data(api_key: str,
                          start_year: str = "2019",
                          end_year: str = "2024") -> list:


    state_series = {
        "Alabama": "LAUST010000000000003", "Alaska": "LAUST020000000000003",
        "Arizona": "LAUST040000000000003", "Arkansas": "LAUST050000000000003",
        "California": "LAUST060000000000003", "Colorado": "LAUST080000000000003",
        "Connecticut": "LAUST090000000000003", "Delaware": "LAUST100000000000003",
        "Florida": "LAUST120000000000003", "Georgia": "LAUST130000000000003",
        "Hawaii": "LAUST150000000000003", "Idaho": "LAUST160000000000003",
        "Illinois": "LAUST170000000000003", "Indiana": "LAUST180000000000003",
        "Iowa": "LAUST190000000000003", "Kansas": "LAUST200000000000003",
        "Kentucky": "LAUST210000000000003", "Louisiana": "LAUST220000000000003",
        "Maine": "LAUST230000000000003", "Maryland": "LAUST240000000000003",
        "Massachusetts": "LAUST250000000000003", "Michigan": "LAUST260000000000003",
        "Minnesota": "LAUST270000000000003", "Mississippi": "LAUST280000000000003",
        "Missouri": "LAUST290000000000003", "Montana": "LAUST300000000000003",
        "Nebraska": "LAUST310000000000003", "Nevada": "LAUST320000000000003",
        "New Hampshire": "LAUST330000000000003", "New Jersey": "LAUST340000000000003",
        "New Mexico": "LAUST350000000000003", "New York": "LAUST360000000000003",
        "North Carolina": "LAUST370000000000003", "North Dakota": "LAUST380000000000003",
        "Ohio": "LAUST390000000000003", "Oklahoma": "LAUST400000000000003",
        "Oregon": "LAUST410000000000003", "Pennsylvania": "LAUST420000000000003",
        "Rhode Island": "LAUST440000000000003", "South Carolina": "LAUST450000000000003",
        "South Dakota": "LAUST460000000000003", "Tennessee": "LAUST470000000000003",
        "Texas": "LAUST480000000000003", "Utah": "LAUST490000000000003",
        "Vermont": "LAUST500000000000003", "Virginia": "LAUST510000000000003",
        "Washington": "LAUST530000000000003", "West Virginia": "LAUST540000000000003",
        "Wisconsin": "LAUST550000000000003", "Wyoming": "LAUST560000000000003",
    }

    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {"Content-type": "application/json"}

    series_ids = list(state_series.values())
    state_names = list(state_series.keys())

    all_records = []

    for i in range(0, len(series_ids), 50):
        batch = series_ids[i:i + 50]
        payload = json.dumps({
            "seriesid": batch,
            "startyear": start_year,
            "endyear": end_year,
            "registrationkey": api_key
        })

        r = requests.post(url, data=payload, headers=headers)
        r.raise_for_status()
        result = r.json()

        for series in result.get("Results", {}).get("series", []):
            sid = series["seriesID"]
            state = state_names[series_ids.index(sid)]
            for item in series["data"]:
                all_records.append({
                    "state": state,
                    "year": int(item["year"]),
                    "month": int(item["period"].replace("M", "")),
                    "unemployment_rate": float(item["value"])
                })

    return all_records


def get_top10_states(records: list) -> list:
    # Calculate average unemployment rate per state
    totals = {}
    counts = {}
    for rec in records:
        state = rec["state"]
        totals[state] = totals.get(state, 0) + rec["unemployment_rate"]
        counts[state] = counts.get(state, 0) + 1

    averages = {state: totals[state] / counts[state] for state in totals}

    # Sort and return top 10
    sorted_states = sorted(averages, key=lambda s: averages[s], reverse=True)
    top10 = sorted_states[:10]

    print("Top 10 states by average unemployment rate (2019-2024):")
    for i, state in enumerate(top10, 1):
        print(f"  {i:2}. {state:<20} {averages[state]:.2f}%")

    return top10


def plot_unemployment_trends(records: list, top10_states: list, result_dir: str = ".") -> None:
    # Convert to DataFrame
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
    df = df.sort_values("date")

    # Filter to top 10 states only
    df = df[df["state"].isin(top10_states)]

    # Plot
    fig, axes = plt.subplots(5, 2, figsize=(14, 18))
    axes = axes.flatten()

    for i, state in enumerate(top10_states):
        state_df = df[df["state"] == state]
        axes[i].plot(state_df["date"], state_df["unemployment_rate"],
                     color="#E63946", linewidth=1.5)
        axes[i].set_title(state, fontsize=11, fontweight="bold")
        axes[i].set_ylabel("Unemployment Rate (%)")
        axes[i].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        axes[i].xaxis.set_major_locator(mdates.YearLocator())
        axes[i].tick_params(axis="x", rotation=45)
        axes[i].grid(True, alpha=0.3)

    fig.suptitle("Monthly Unemployment Rate (2019-2024)\nTop 10 Highest-Unemployment States",
                 fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(f"{result_dir}/unemployment_trends.png", dpi=150, bbox_inches="tight")
    print("Saved: unemployment_trends.png")
    plt.close()