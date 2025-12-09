# analysis.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# analysis scripts on games_with_weather


def main():
    os.makedirs("results", exist_ok=True)

    df = pd.read_csv("data/processed/games_with_weather.csv")

    # drop games without weather
    df = df.dropna(subset=["temperature"])

    # total points
    df["total_points"] = df["home_points"] + df["away_points"]


    # analysis 1: how do total points vary with temperature

    # temperature is in celsius from open-meteo, so:
    #   very_cold:   temp < 5c
    #   cold:        5c <= temp < 15c
    #   mild:        15c <= temp < 25c
    #   hot:         temp >= 25c

    def temp_bin(t):
        if t < 5:
            return "very_cold"
        elif t < 15:
            return "cold"
        elif t < 25:
            return "mild"
        else:
            return "hot"

    df["temp_bin"] = df["temperature"].apply(temp_bin)

    grouped = (df.groupby("temp_bin")["total_points"].agg(["count", "mean"]).reset_index().sort_values("temp_bin"))

    grouped.to_csv("results/points_vs_temp_stats.csv", index=False)

    plt.figure(figsize=(6, 4))
    plt.bar(grouped["temp_bin"], grouped["mean"])
    plt.xlabel("temperature bin (c)")
    plt.ylabel("average total points")
    plt.title("average total points by temperature bin")
    plt.tight_layout()
    plt.savefig("results/points_vs_temp.png")
    plt.close()

    

    # analysis 2: relationship between temperature and total points

    plt.figure(figsize=(7, 5))
    plt.scatter(df["temperature"], df["total_points"], alpha=0.4)

    # fit simple linear regression
    m, b = np.polyfit(df["temperature"], df["total_points"], 1)

    # regression line
    xs = np.linspace(df["temperature"].min(), df["temperature"].max(), 100)
    ys = m * xs + b
    plt.plot(xs, ys, color="red", label=f"trend line: y = {m:.2f}x + {b:.1f}")

    plt.xlabel("temperature (c)")
    plt.ylabel("total points scored")
    plt.title("relationship between temperature and scoring")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/temp_vs_points_regression.png")
    plt.close()

if __name__ == "__main__":
    main()