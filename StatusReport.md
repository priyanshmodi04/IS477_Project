# Milestone 3 – Interim Status Report  
**Project:** Weather and College Football Performance  
**Course:** IS 477 Team Project  
**Team Members:** Priyansh Modi and Shivam Patel  

---

## Project Overview

This team project attempts to understand the relationship between weather and on-field performance for NCAA football games across the United States. By combining statistics from the CollegeFootballData API with Open-Meteo historical weather information, we assess how temperature, wind speed, and precipitation impact points, turnovers, and yardage (i.e., offensive/defensive success).

The project follows a full data lifecycle (acquisition, storage, integration, quality control, analysis, reproducibility). This report summarizes the status of each planned task, provides an updated timeline, documents revisions to the plan, and describes what each team member has contributed so far.

---

## Status by Task (Compared to Planned Schedule)

### Week 1–2: Lifecycle, Research Questions, and Data Acquisition

We chose to work within the **Data Curation Lifecycle** model and documented our application of it. Our research questions, ethics considerations, and API usage notes are in the project plan.

We implemented a Python script (`data.py`) that now handles all acquisition tasks:

- `fetch_games()` retrieves game info  
- `fetch_venues()` retrieves stadium coordinates  
- `merge_games_with_venues()` joins games and venues  
- `fetch_weather()` retrieves hourly weather  
- `get_weather_for_game()` finds nearest weather to kickoff  
- `merge_all_weather()` attaches weather to each game  

Responses are stored in `data/` and the script automatically outputs a combined CSV (`games_with_weather.csv`).

**Status:** Completed.

---

### Week 3: Storage, Organization, and Feature Extraction

We defined the storage model with **raw / intermediate / final** folders and documented naming conventions.

With the updated script, feature extraction is simpler and now handled directly inside `data.py` using:

- Cleaned game-level variables (team names, points, start time)
- Latitude/longitude via venue merge
- Hourly temperature, precipitation, and wind speed pulled from Open-Meteo

A merged dataset is automatically produced once the script runs end-to-end.

**Status:** Mostly completed.

---

### Week 4: Integration and Provenance

The new script provides a cleaner integration workflow using:

- `merge_games_with_venues()` for coordinates  
- `merge_all_weather()` to attach nearest hourly weather values

We validated joins in a Jupyter notebook by inspecting games from different regions and checking the weather readings for correctness.

We also started an integration log summarizing:

- Input files  
- Script behavior and version  
- Join keys (venue + date)  

We still need to finish checking the percentage of games missing weather or coordinates and document how those will be handled.

**Status:** In progress.

---

### Week 5: Quality and Cleaning

Preliminary data-quality checks were run in a notebook. These checks recorded missingness in:

- Home/away points  
- Turnovers (if added later)  
- Weather variables (temperature, precipitation, wind_speed)

A draft quality report was started. Some weather readings may be missing due to API gaps or stadiums with no coordinates.

Next steps include finalizing rules for dealing with incomplete weather records and applying them before modeling.

**Status:** Partially completed.

---

### Week 6: Pre-Analysis, Exploratory Analysis, and Automation

We began exploratory analysis with scatterplots comparing weather and performance metrics, such as temperature vs. total points and wind speed vs. turnovers.

A reusable module structure was started so loading and cleaning functions from `data.py` can be reused across notebooks.

A basic pipeline was also started inside `data.py` (running end-to-end under `if __name__ == '__main__':`) so that one command reproduces:

1. Game acquisition  
2. Venue acquisition  
3. Merging  
4. Weather retrieval  
5. Exporting a final CSV  

Next steps include finishing the automation layer and running regression models.

**Status:** In progress.

---

### Weeks 7–9: Pending Work

Remaining work includes:

- Final cleaning steps  
- Correlation and regression modeling  
- More robust reproducibility (requirements file, clearer instructions)  
- Final report and data dictionary  
- Visualizations  
- Tagged release  

**Status:** Planned.

---

## Updated Project Timeline and Task Progress

- **Lifecycle model + research questions:** Completed (Week 1)  
- **Acquire CollegeFootballData games/venues:** Completed (Week 2)  
- **Acquire Open-Meteo weather:** Completed using `data.py` (Week 3, refinements ongoing)  
- **Determine storage model:** Completed (Week 3)  
- **Extract football + weather features:** First draft complete, updated via `data.py`  
- **Join game + weather data:** Running end-to-end; validation ongoing  
- **Data quality assessment:** First pass done; final cleaning due Week 7  
- **Exploratory analysis:** In progress (Weeks 6–7)  
- **Pipeline + reproducibility:** Started inside `data.py`; expanding in Weeks 7–8  
- **Regression modeling:** Planned Weeks 8–9  
- **Final documentation, README, dictionary, release:** Week 9  

---

## Changes to the Project Plan

### Scope Adjustments

We limited the dataset to recent seasons to reduce inconsistencies and simplify integration.  
The main weather predictors remain: **temperature, wind speed, precipitation**.  
Secondary predictors (like humidity) will only be explored descriptively.

### Methodology Adjustments

We clarified that the **unit of analysis is the game**, not the play. All weather is aggregated to game-level using nearest-hour matching from the API.

Region vs. team performance is confounded, so team strength (win percentage or scoring margin) will be used to adjust comparisons. Region will be secondary.

### Reproducibility Improvements

The updated `data.py` script now:

- Automatically fetches all data  
- Performs all merging  
- Retrieves hourly weather  
- Produces a final combined CSV  

A workflow diagram will be added soon. A more formal workflow tool may be added if time permits.

---

## Individual Contributions for This Milestone

### **Priyansh Modi**

 focused on **data acquisition, storage structure, and integration**:

- Implemented all new API calls inside `data.py`  
- Handled API parameters, rate limits, and merging  
- Built the full end-to-end script that outputs `games_with_weather.csv`  
- Set up the directory structure and file organization  
- Started the automation pipeline and integration documentation  

### **Shivam Patel**

 focused on **feature selection, validation, EDA, and documentation**:

- Reviewed and validated the merged dataset produced by `data.py`  
- Ran data-quality checks and drafted the quality report  
- Created early exploratory plots (weather vs scoring/turnovers)  
- Helped test weather-match accuracy (nearest-hour logic)  
- Wrote and organized most of the milestone documentation  

---
