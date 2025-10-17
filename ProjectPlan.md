Priyansh Modi, Shivam Patel

IS 477

Project Plan

16 October 2025

Overview

This projects investigates how weather conditions influence offensice and defensive performance in college football games across the United States. Given that football is an outdoor sport, environmental factors such as, temperature, wind speed, humidity, and precipitation, all affect how the game is played. These factors can influence play calls, ball control, turnover rates, and overall scoring. By combining structured sports statistics and with real-world weather data, this project aims to quantify whether and how weather impacts total points scored, turnovers, and yardage gained.

This project will implement the complete data lifecycle pipeline:

Acquistion: Pull data from two API sources.

Storage: Save JSON responses into CSV tables.

Integration: Join game stats with corresponding weather conditions using the coordinates of the stadium and dates.

Quality assessment: Handle missing/unstructured data and check for consistency.

Reproducibility: Provide scripts and documentation to reproduce the workflow end-to-end.

Research questions

How do temperature, wind speed, and precipitation affect offensive performance in college football games?

Are certain weather conditions associated with increased turnovers?

Do teams from colder regions perform relatively better than warmer-region teams under “bad” weather conditions?

Team members

Priyansh Modi

Acquire raw data from the CollegeFootballData API and Open-Meteo API using Python.

Handle data stroage/organization, converting API JSON to CSV.

Integrate datasets by matching game records with corresponding weather data.

Maintain Github documentation on dataset structure

Shivam Patel

Conduct data cleaning and assess quality (handle missing values, validate coordindates, etc.)

Perform EDA, correlation, and regression modeling.

Create visualizations showing relationships between weather and performance metrics.

Write portions of the project report related to analysis of findings and visual interpretations.

Datasets

CollegeFootballData API

https://api.collegefootballdata.com/?utm_source=chatgpt.com

This will be accessed through a REST API, and the data contains game schedules, team names, stadium information, game statistics, and other metadata including season, week, home/away games, etc.

Open-Meteo Historical Weather API

https://open-meteo.com/en/docs/historical-weather-api

This will be accessed through a REST API as well. This data source contains historical hourly and daily data on temperature, wind speed, precipitation, humidity etc. It required latitudes and longitudes for the stadiums that will be obtained from the CollegeFootballData “venues” endpoint.

We plan on using the venues endpoint to get each stadium’s longitude and latitude and then query the Open-Meteo API for weather data corresponding to each game’s data and location.

Timeline

Week 1: Data Lifecycle + Acquisition: Priyansh Modi and Shivam Patel

Select a lifecycle model (Data Curation Lifecycle) and map it to our specefic workflow.

Define research questions and outline ethical data handling (check license checks for APIs)

Acquire first dataset from CollegeFootballData API

Document API access, endpoint structure

Week 2: Module 3 Continued: Priyansh Modi and Shivam Patel

Acquire second dataset from Open-Meteo APII. Priyansh

Collect sample JSON responses; convert to CSV for preview. Shivam

Verify both sources meet the “distinct format/source” requirement. Shivam

Week 3: Storage, Organization, and Extraction/Enrichment: Priyansh Modi and Shivam Patel

Define storage model (tabular CSV, metadata JSON) Priyansh

Establish naming conventions and Github directory structure Priyansh

Extract relevant variables (yards, turnovers, weather metrics) Shivam

Enrich data with stadium latitude/longitude for later joins. Shivam

Week 4: Data Integration: Priyansh Modi and Shivam Patel

Merge football and weather datasets using game data and stadium coordinates. Priyansh

Validate joins with random samples. Shivam

Record provenance in a data integration log markdown file. Shivam

Week 5: Data Quality and Cleaning: Priyansh Modi

Assess completeness, identify and handle outliers, and document data-quality metrics

Week 6: Pre-Analysis + Modules 11 and 12 Intro: Automation and Provenance:

Begin EDA. Shivam

Develop jupyter notebooks/python scripts. Both

Start automating the workflow using a master script. Priyansh

Week 7: Modules 11 and 12 continued

Add timestamps/file checksums for reproducibility. Both

Verify execution. Both

Update Git commits. Priyansh

Week 8: Reproducibility and Transparency

Create a README.md detailing setup, dependencies, and reproduction steps. Priyansh

Generate a requirments.txt file. Priyansh

Make pushes to GitHub. Priyansh

Week 9: Metadata and Documentation + Final Report

Prepare final report. Both

Create data dictionary/codebook and desciptive metadata. Shivam

Package all visualizations. Shivam

Publish final tagged release. Priyansh

Constaints

Both APIs limit daily calls so caching responses will be necessary.

Incomplete or missing weather records are bound for some games.

Stadium coordinates and game start times must match local weather timestamps accurately.

Data will be properly cited despite both APIs being open and having clear license permissions.

Gaps and Future Needs

Validation against NOAA Climate Data may be required if Open-Meteo results are incomplete

Potential extension: Adding attendance data for further analysis of weather’s impact on fan engagement.
