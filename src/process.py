from load import get_top10_states
import pandas as pd


def process_unemployment_records(records: list) -> tuple:
    top10_states = get_top10_states(records)

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
    df = df.sort_values("date")
    df = df[df["state"].isin(top10_states)]

    return df, top10_states
