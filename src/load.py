import time
import random
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pytrends.request import TrendReq
from config import (BLS_API_URL, TRENDS_TIMEFRAME, TRENDS_MIN_DELAY, TRENDS_MAX_DELAY,
                    FUNCTIONAL_KEYWORDS, RECREATIONAL_KEYWORDS)

# Get the data of unemployment rate from BLS
def get_unemployment_data(api_key, start_year="2019", end_year="2024"):
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

    headers = {"Content-type": "application/json"}
    series_ids = list(state_series.values())
    state_names = list(state_series.keys())

    start = int(start_year)
    end = int(end_year)
    year_batches = []
    while start <= end:
        batch_end = min(start + 2, end)
        year_batches.append((str(start), str(batch_end)))
        start = batch_end + 1

    all_records = []
    for (y_start, y_end) in year_batches:
        print(f"Fetching BLS data {y_start}-{y_end}...")
        for i in range(0, len(series_ids), 50):
            batch = series_ids[i:i + 50]
            payload = json.dumps({
                "seriesid": batch,
                "startyear": y_start,
                "endyear": y_end,
                "registrationkey": api_key
            })
            r = requests.post(BLS_API_URL, data=payload, headers=headers)
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

#Caculate the average of unemployment rate and rank top 10
def get_top10_states(records):
    totals = {}
    counts = {}
    for rec in records:
        state = rec["state"]
        totals[state] = totals.get(state, 0) + rec["unemployment_rate"]
        counts[state] = counts.get(state, 0) + 1

    averages = {state: totals[state] / counts[state] for state in totals}
    sorted_states = sorted(averages, key=lambda s: averages[s], reverse=True)
    top10 = sorted_states[:10]

    print("Top 10 states by average unemployment rate:")
    for i, state in enumerate(top10, 1):
        print(f"  {i}. {state} {averages[state]:.2f}%")

    return top10

STATE_GEO_CODES = {
    "Nevada": "US-NV", "California": "US-CA", "New York": "US-NY",
    "Illinois": "US-IL", "Alaska": "US-AK", "Michigan": "US-MI",
    "New Jersey": "US-NJ", "New Mexico": "US-NM", "Washington": "US-WA",
    "Louisiana": "US-LA", "Rhode Island": "US-RI", "Connecticut": "US-CT",
    "Mississippi": "US-MS", "Arizona": "US-AZ", "Oregon": "US-OR",
    "Kentucky": "US-KY", "Texas": "US-TX", "Georgia": "US-GA",
    "Hawaii": "US-HI", "Massachusetts": "US-MA", "Delaware": "US-DE",
    "Pennsylvania": "US-PA",
}

#Get functional and recreational data from Google trends
def get_trends_data(states, keywords, category, timeframe=TRENDS_TIMEFRAME,
                    min_delay=TRENDS_MIN_DELAY, max_delay=TRENDS_MAX_DELAY):
    pytrends = TrendReq(hl="en-US", tz=360)
    all_records = []

    for state in states:
        geo = STATE_GEO_CODES.get(state)
        if not geo:
            print(f"Skipping {state}: no geo code found")
            continue

        print(f"Fetching {category} trends for {state}...")
        try:
            pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
            df = pytrends.interest_over_time()

            if df.empty:
                print(f"No data for {state}")
                continue

            df = df.drop(columns=["isPartial"], errors="ignore")

            for keyword in keywords:
                if keyword not in df.columns:
                    continue
                for date, value in df[keyword].items():
                    all_records.append({
                        "state": state,
                        "year": date.year,
                        "month": date.month,
                        "keyword": keyword,
                        "search_index": int(value),
                        "category": category
                    })

# AI(Claude) generated: random delay to avoid rate limiting from Google Trends
            delay = random.uniform(min_delay, max_delay)
            print(f"Waiting {delay:.1f}s...")
            time.sleep(delay)

        except Exception as e:
            if "429" in str(e):
                print(f"Rate limited! Waiting 60s before retrying {state}...")
                time.sleep(60)
                try:
                    pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
                    df = pytrends.interest_over_time()
                    if not df.empty:
                        df = df.drop(columns=["isPartial"], errors="ignore")
                        for keyword in keywords:
                            if keyword not in df.columns:
                                continue
                            for date, value in df[keyword].items():
                                all_records.append({
                                    "state": state,
                                    "year": date.year,
                                    "month": date.month,
                                    "keyword": keyword,
                                    "search_index": int(value),
                                    "category": category
                                })
                except Exception as e2:
                    print(f"Retry failed for {state}: {e2}")
            else:
                print(f"Error fetching {state}: {e}")
            time.sleep(random.uniform(min_delay, max_delay))
            continue

    return all_records


def get_functional_trends(top10_states):
    print("\nFetching Functional Trends (LinkedIn, Job, Hiring)...")
    return get_trends_data(top10_states, FUNCTIONAL_KEYWORDS, "functional")


def get_recreational_trends(top10_states):
    print("\nFetching Recreational Trends (TikTok, Netflix, Instagram)...")
    return get_trends_data(top10_states, RECREATIONAL_KEYWORDS, "recreational")

#Plot part
def plot_unemployment_trends(records, top10_states, result_dir="."):
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
    df = df.sort_values("date")
    df = df[df["state"].isin(top10_states)]

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
    plt.show()
    plt.close()


def plot_trends_comparison(unemployment_records, trends_records, top10_states,
                           category, result_dir="."):
    unemp_df = pd.DataFrame(unemployment_records)
    unemp_df["date"] = pd.to_datetime(unemp_df[["year", "month"]].assign(day=1))
    unemp_df = unemp_df[unemp_df["state"].isin(top10_states)]

    trends_df = pd.DataFrame(trends_records)
    trends_df["date"] = pd.to_datetime(trends_df[["year", "month"]].assign(day=1))
    trends_avg = trends_df.groupby(["state", "date"])["search_index"].mean().reset_index()

    fig, axes = plt.subplots(5, 2, figsize=(14, 18))
    axes = axes.flatten()

    color_unemp = "#E63946"
    color_trends = "#2196F3" if category == "functional" else "#4CAF50"

    for i, state in enumerate(top10_states):
        ax1 = axes[i]
        ax2 = ax1.twinx()

        u_df = unemp_df[unemp_df["state"] == state].sort_values("date")
        t_df = trends_avg[trends_avg["state"] == state].sort_values("date")

        ax1.plot(u_df["date"], u_df["unemployment_rate"],
                 color=color_unemp, linewidth=1.5, label="Unemployment Rate")
        ax2.plot(t_df["date"], t_df["search_index"],
                 color=color_trends, linewidth=1.5, linestyle="--", label="Search Index")

        ax1.set_title(state, fontsize=11, fontweight="bold")
        ax1.set_ylabel("Unemployment Rate (%)", color=color_unemp)
        ax2.set_ylabel("Search Index", color=color_trends)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax1.xaxis.set_major_locator(mdates.YearLocator())
        ax1.tick_params(axis="x", rotation=45)
        ax1.grid(True, alpha=0.3)

    title = "Functional" if category == "functional" else "Recreational"
    fig.suptitle(f"Unemployment Rate vs. {title} Social Media Search Interest (2019-2024)",
                 fontsize=12, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(f"{result_dir}/{category}_trends_comparison.png", dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Saved: {category}_trends_comparison.png")
    plt.close()


def plot_average_trends(unemployment_records, functional_records, recreational_records,
                        top10_states, result_dir="."):
    unemp_df = pd.DataFrame(unemployment_records)
    unemp_df["date"] = pd.to_datetime(unemp_df[["year", "month"]].assign(day=1))
    unemp_df = unemp_df[unemp_df["state"].isin(top10_states)]
    unemp_avg = unemp_df.groupby("date")["unemployment_rate"].mean().reset_index()

    func_df = pd.DataFrame(functional_records)
    func_df["date"] = pd.to_datetime(func_df[["year", "month"]].assign(day=1))
    func_avg = func_df.groupby("date")["search_index"].mean().reset_index()

    rec_df = pd.DataFrame(recreational_records)
    rec_df["date"] = pd.to_datetime(rec_df[["year", "month"]].assign(day=1))
    rec_avg = rec_df.groupby("date")["search_index"].mean().reset_index()

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    ax1.plot(unemp_avg["date"], unemp_avg["unemployment_rate"],
             color="#E63946", linewidth=2.5, label="Avg Unemployment Rate")
    ax2.plot(func_avg["date"], func_avg["search_index"],
             color="#2196F3", linewidth=2, linestyle="--", label="Functional Avg (LinkedIn/Job/Hiring)")
    ax2.plot(rec_avg["date"], rec_avg["search_index"],
             color="#4CAF50", linewidth=2, linestyle=":", label="Recreational Avg (TikTok/Netflix/Instagram)")

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Unemployment Rate (%)", color="#E63946")
    ax2.set_ylabel("Search Index", color="gray")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(True, alpha=0.3)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=10)

    ax1.set_title("Average Trends Across Top 10 States (2019-2024)\n"
                  "Unemployment Rate vs. Social Media Search Interest",
                  fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{result_dir}/average_trends.png", dpi=150, bbox_inches="tight")
    print("Saved: average_trends.png")
    plt.show()
    plt.close()