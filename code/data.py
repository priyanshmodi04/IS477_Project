# data.py

import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv() 

CFB_API_KEY = os.getenv("CFB_API_KEY")
CFB_API_BASE = "https://apinext.collegefootballdata.com"
WEATHER_API_BASE = "https://archive-api.open-meteo.com/v1/archive"


#getting games
def fetch_games(season: int, week: int) -> pd.DataFrame:
    """Fetch clean game-level data from the APINext CollegeFootballData API."""

    url = f"{CFB_API_BASE}/games"
    params = {
        "year": season,       
        "week": week,
        "seasonType": "regular"
    }

    headers = {
        "Authorization": f"Bearer {CFB_API_KEY}"
    }

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    games = []
    for g in data:
        games.append({
            "game_id": g.get("id"),
            "season": g.get("season"),
            "week": g.get("week"),
            "start_time": g.get("startDate"),
            "venue": g.get("venue"),
            "home_team": g.get("homeTeam"),
            "away_team": g.get("awayTeam"),
            "home_points": g.get("homePoints"),
            "away_points": g.get("awayPoints")
        })

    return pd.DataFrame(games)


#getting venues
def fetch_venues() -> pd.DataFrame:
    """Retrieve all venue info including latitude and longitude."""
    url = f"{CFB_API_BASE}/venues"
    
    headers = {"Authorization": f"Bearer {CFB_API_KEY}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    
    data = resp.json()
    venues = []

    for v in data:
        venues.append({
            "venue": v.get("name"),
            "city": v.get("city"),
            "state": v.get("state"),
            "latitude": v.get("latitude"),
            "longitude": v.get("longitude")
        })

    return pd.DataFrame(venues)


#merging games and venues (lat/lon)
def merge_games_with_venues(games_df, venues_df):
    """Join game data with venue coordinates."""
    merged = games_df.merge(
        venues_df,
        on="venue",
        how="left"
    )
    return merged


#Fetching weather for data/range
def fetch_weather(latitude: float, longitude: float, start_date: str) -> pd.DataFrame:
    """Fetch hourly weather data for one calendar day."""
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "start_date": start_date,
        "end_date": start_date     # same day
    }

    resp = requests.get(WEATHER_API_BASE, params=params)
    resp.raise_for_status()
    wdata = resp.json()

    df = pd.DataFrame({
        "datetime": wdata["hourly"]["time"],
        "temperature": wdata["hourly"]["temperature_2m"],
        "precipitation": wdata["hourly"]["precipitation"],
        "wind_speed": wdata["hourly"]["wind_speed_10m"]
    })

    return df


# -------------------------------------------------------------------
# 5. GET WEATHER NEAREST TO GAME START TIME
# -------------------------------------------------------------------
def get_weather_for_game(row):
    """Fetch weather for a single game based on venue lat/lon + kickoff time."""
    
    lat = row["latitude"]
    lon = row["longitude"]

    if pd.isna(lat) or pd.isna(lon):
        return pd.Series({"temperature": None, "precipitation": None, "wind_speed": None})

    # Extract YYYY-MM-DD from start time
    date_str = row["start_time"][:10]

    weather = fetch_weather(lat, lon, date_str)

    # Convert to datetime
    kickoff = pd.to_datetime(row["start_time"]).tz_localize(None)
    weather["datetime"] = pd.to_datetime(weather["datetime"])

    # Closest hourly reading
    closest = weather.iloc[(weather["datetime"] - kickoff).abs().argsort().iloc[0]]

    return pd.Series({
        "temperature": closest["temperature"],
        "precipitation": closest["precipitation"],
        "wind_speed": closest["wind_speed"]
    })

#merging weather with each game
def merge_all_weather(games_with_coords):
    weather_rows = games_with_coords.apply(get_weather_for_game, axis=1)
    full_df = pd.concat([games_with_coords, weather_rows], axis=1)
    return full_df



if __name__ == "__main__":
    games_df = fetch_games(season=2023, week=1)
    print(games_df.head(), "\n")

    venues_df = fetch_venues()
    print(venues_df.head(), "\n")

    games_with_coords = merge_games_with_venues(games_df, venues_df)
    print(games_with_coords.head(), "\n")

    full_df = merge_all_weather(games_with_coords)
    print(full_df.head(), "\n")

    #csv
    os.makedirs("data", exist_ok=True)
    full_df.to_csv("data/games_with_weather.csv", index=False)
    
