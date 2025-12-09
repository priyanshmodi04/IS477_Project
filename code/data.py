# data.py

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

CFB_API_KEY = os.getenv("CFB_API_KEY")
CFB_API_BASE = "https://apinext.collegefootballdata.com"
WEATHER_API_BASE = "https://archive-api.open-meteo.com/v1/archive"

# seasons and weeks to pull
SEASONS = list(range(2020, 2024))   # 2020–2023
WEEKS = [1, 2]                      # first two weeks only


# getting games for a single week
def fetch_games(season: int, week: int) -> pd.DataFrame:
    """fetch game-level data for a single season/week"""

    url = f"{CFB_API_BASE}/games"
    params = {
        "year": season,
        "week": week,
        "seasonType": "regular",
    }
    headers = {"Authorization": f"Bearer {CFB_API_KEY}"}

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
            "away_points": g.get("awayPoints"),
        })

    return pd.DataFrame(games)


# getting games for multiple weeks in a season
def fetch_games_for_season(season: int, weeks: list[int]) -> pd.DataFrame:
    """fetch all games for a season for the specified weeks"""

    all_weeks = []

    for week in weeks:
        try:
            df = fetch_games(season, week)
        except requests.HTTPError as e:
            print(f"[warn] error fetching season {season}, week {week}: {e}")
            continue

        if df is None or df.empty:
            print(f"[info] no games for season {season}, week {week}")
            continue

        print(f"[info] retrieved {len(df)} games for season {season}, week {week}")
        all_weeks.append(df)

    if not all_weeks:
        print(f"[warn] no games found for season {season}")
        return pd.DataFrame()

    return pd.concat(all_weeks, ignore_index=True)


# getting venue information
def fetch_venues() -> pd.DataFrame:
    """fetch venue data including latitude/longitude"""

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
            "longitude": v.get("longitude"),
        })

    return pd.DataFrame(venues)


# merging game data with venue coordinates
def merge_games_with_venues(games_df: pd.DataFrame,
                            venues_df: pd.DataFrame) -> pd.DataFrame:
    """merge games with venue lat/lon"""

    merged = games_df.merge(
        venues_df,
        on="venue",
        how="left",
        suffixes=("", "_venue"),
    )
    return merged


# fetching hourly weather for a specific date and location
def fetch_weather(latitude: float, longitude: float, date_str: str) -> pd.DataFrame:
    """fetch hourly weather for one day"""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "start_date": date_str,
        "end_date": date_str,
    }

    resp = requests.get(WEATHER_API_BASE, params=params)
    resp.raise_for_status()
    wdata = resp.json()

    if "hourly" not in wdata or "time" not in wdata["hourly"]:
        return pd.DataFrame(columns=[
            "datetime", "temperature", "precipitation", "wind_speed"
        ])

    df = pd.DataFrame({
        "datetime": wdata["hourly"]["time"],
        "temperature": wdata["hourly"]["temperature_2m"],
        "precipitation": wdata["hourly"]["precipitation"],
        "wind_speed": wdata["hourly"]["wind_speed_10m"],
    })

    return df


# building a weather cache keyed by (lat, lon, date)
def build_weather_cache(games_with_coords: pd.DataFrame) -> dict:
    """fetch weather once per (lat, lon, date) and store in a cache"""

    keys = set()

    for _, row in games_with_coords.iterrows():
        lat = row.get("latitude")
        lon = row.get("longitude")
        start_time = row.get("start_time")

        if pd.isna(lat) or pd.isna(lon):
            continue
        if not start_time or len(start_time) < 10:
            continue

        date_str = start_time[:10]
        key = (float(lat), float(lon), date_str)
        keys.add(key)

    keys = list(keys)
    print(f"[info] unique (lat, lon, date) combos for weather: {len(keys)}")

    cache = {}

    for lat, lon, date_str in tqdm(keys, desc="fetching weather batches"):
        try:
            df = fetch_weather(lat, lon, date_str)
        except requests.HTTPError as e:
            print(f"[warn] weather fetch failed for ({lat}, {lon}, {date_str}): {e}")
            df = pd.DataFrame(columns=[
                "datetime", "temperature", "precipitation", "wind_speed"
            ])
        cache[(lat, lon, date_str)] = df

    return cache


# closest weather to kickoff using cache
def get_weather_for_game(row: pd.Series, cache: dict) -> pd.Series:
    """find weather closest to kickoff time using cached daily data"""

    lat = row.get("latitude")
    lon = row.get("longitude")

    if pd.isna(lat) or pd.isna(lon):
        return pd.Series({"temperature": None, "precipitation": None, "wind_speed": None})

    start_time = row.get("start_time")
    if not start_time or len(start_time) < 10:
        return pd.Series({"temperature": None, "precipitation": None, "wind_speed": None})

    date_str = start_time[:10]
    key = (float(lat), float(lon), date_str)

    weather = cache.get(key)
    if weather is None or weather.empty:
        return pd.Series({"temperature": None, "precipitation": None, "wind_speed": None})

    try:
        kickoff = pd.to_datetime(start_time).tz_localize(None)
    except Exception:
        return pd.Series({"temperature": None, "precipitation": None, "wind_speed": None})

    weather = weather.copy()
    weather["datetime"] = pd.to_datetime(weather["datetime"])
    closest = weather.iloc[(weather["datetime"] - kickoff).abs().argsort().iloc[0]]

    return pd.Series({
        "temperature": closest["temperature"],
        "precipitation": closest["precipitation"],
        "wind_speed": closest["wind_speed"],
    })


# applying weather to each game row with progress bar
def merge_all_weather(games_with_coords: pd.DataFrame) -> pd.DataFrame:
    """apply weather lookup to each game with batching and progress bar"""

    # build cache of daily weather per (lat, lon, date)
    weather_cache = build_weather_cache(games_with_coords)

    weather_rows = []
    for _, row in tqdm(
        games_with_coords.iterrows(),
        total=len(games_with_coords),
        desc="matching weather to games"
    ):
        weather_rows.append(get_weather_for_game(row, weather_cache))

    weather_df = pd.DataFrame(weather_rows)
    return pd.concat([games_with_coords.reset_index(drop=True), weather_df], axis=1)


# main workflow
if __name__ == "__main__":

    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # venues
    print("[info] fetching venues...")
    venues_df = fetch_venues()
    venues_df.to_csv("data/raw/venues_all.csv", index=False)
    print(f"[info] saved venues (rows={len(venues_df)})")

    # games for each season
    all_games = []
    for season in SEASONS:
        print(f"[info] fetching season {season}...")
        games_df = fetch_games_for_season(season, WEEKS)

        if games_df.empty:
            print(f"[warn] no games found for season {season}")
            continue

        path = f"data/raw/games_{season}_weeks_{'-'.join(map(str, WEEKS))}.csv"
        games_df.to_csv(path, index=False)
        print(f"[info] saved {len(games_df)} games for season {season}")

        all_games.append(games_df)

    if not all_games:
        raise SystemExit("[error] no games found across all seasons")

    games_all = pd.concat(all_games, ignore_index=True)
    print(f"[info] total games across seasons: {len(games_all)}")

    # merge with coords
    print("[info] merging games with venue coords...")
    games_with_coords = merge_games_with_venues(games_all, venues_df)
    coords_path = "data/processed/games_with_coords.csv"
    games_with_coords.to_csv(coords_path, index=False)
    print(f"[info] saved merged file (rows={len(games_with_coords)})")

    # weather lookup (batched + progress bars)
    print("[info] fetching weather for each game (batched)...")
    full_df = merge_all_weather(games_with_coords)

    # final save
    final_path = "data/processed/games_with_weather.csv"
    full_df.to_csv(final_path, index=False)
    full_df.to_csv("data/games_with_weather.csv", index=False)  # compatibility

    print(f"[info] saved final dataset (rows={len(full_df)})")