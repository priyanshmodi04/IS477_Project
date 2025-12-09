# quality.py

import os
import pandas as pd

# data quality summary for games_with_weather

def main():
    os.makedirs("results", exist_ok=True)

    df = pd.read_csv("data/processed/games_with_weather.csv")

    # total points
    df["total_points"] = df["home_points"] + df["away_points"]

    # fields to check for missing values
    key_cols = [
        "game_id",
        "season",
        "week",
        "start_time",
        "venue",
        "home_team",
        "away_team",
        "home_points",
        "away_points",
        "latitude",
        "longitude",
        "temperature",
        "precipitation",
        "wind_speed",
    ]

    rows = []

    # basic info
    rows.append({"metric": "row_count", "value": len(df)})

    # missing counts
    for col in key_cols:
        missing = df[col].isna().sum()
        rows.append({"metric": f"missing_{col}", "value": int(missing)})

    # basic ranges / sanity checks
    rows.append({"metric": "min_total_points", "value": float(df["total_points"].min())})
    rows.append({"metric": "max_total_points", "value": float(df["total_points"].max())})

    if "temperature" in df.columns:
        rows.append({"metric": "min_temperature_c", "value": float(df["temperature"].min())})
        rows.append({"metric": "max_temperature_c", "value": float(df["temperature"].max())})

    if "wind_speed" in df.columns:
        rows.append({"metric": "min_wind_speed", "value": float(df["wind_speed"].min())})
        rows.append({"metric": "max_wind_speed", "value": float(df["wind_speed"].max())})

    if "precipitation" in df.columns:
        rows.append({"metric": "min_precipitation", "value": float(df["precipitation"].min())})
        rows.append({"metric": "max_precipitation", "value": float(df["precipitation"].max())})

    summary = pd.DataFrame(rows)
    summary.to_csv("results/data_quality_summary.csv", index=False)


if __name__ == "__main__":
    main()