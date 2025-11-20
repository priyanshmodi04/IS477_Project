# Milestone 3 – Interim Status Report  
**Project:** Weather and College Football Performance  
**Course:** IS 477 Team Project  
**Team Members:** Priyansh Modi and Shivam Patel  



## Project Overview

This team project attempts to understand the relationship between weather and on-field performance for NCAA football games across the United States. By combining statistics from the CollegeFootballData API with Open-Meteo historical weather information, we assess how temperature (relative and actual), wind speed, and precipitation impact points, turnovers, and yardage (i.e., offensive/defensive success).

The project follows a full data lifecycle (acquisition, storage, integration, quality control, analysis, and reproducibility). This report summarizes the status of each planned task, provides an updated timeline, documents revisions to the plan, and describes what each team member has contributed so far.



## Status by Task (Compared to Planned Schedule)

### Week 1–2: Lifecycle, Research Questions, and Data Acquisition

We chose to work within the **Data Curation Lifecycle** model and documented our application of it in a short design document. Our research questions, ethics considerations, and usage notes for both APIs are documented in the project plan.

We implemented a Python script to acquire game data and stadium location information from the CollegeFootballData API, and to sample weather data from the Open-Meteo API. Responses are stored in a `data/raw` directory, and we created short notes describing which endpoint we used for each component.  





### Week 3: Storage, Organization, and Feature Extraction

We defined a storage model with **raw / intermediate / final** folders and established the repository naming conventions. This directory structure and naming scheme are documented in the repo.

Feature-extraction scripts pull together the primary football variables (result, yards gained/lost, turnovers) and primary weather variables:

- Temperature (nominal and ordinal)
- Wind speed and duration
- Precipitation (nominal days without rain, ordinal days with mild vs. heavy rain)

These are stored in concise CSVs. A merged file was also created that provides latitude/longitude locations for each game for use in later joins.

**Status:** Mostly completed (feature definitions may still be refined).



### Week 4: Integration and Provenance

We created an integration script that joins the game and weather feature tables using stadium and date to create a new table that includes both types of variables. We began testing the joins in a Jupyter notebook by checking games across different regions and months to see if the assigned weather values make sense.

We also started an integration log that records:

- Which files were used for integration  
- The integration script version  
- The keys through which tables were joined  

The integration currently works end-to-end, with two caveats:

1. We still need to quantify the percentage of successful matches.  
2. We need to clearly document what we will do in cases where games do not have accompanying weather data.

A CSV file has also been created to guide handling of missing values.

**Status:** In progress.



### Week 5: Quality and Cleaning

We performed preliminary data-quality checks in an additional Jupyter notebook. This notebook tracks key variables (e.g., game points, turnovers) and summarizes their missingness levels for use in our eventual data-quality report. It also flags obvious outliers (for example, temperatures outside a realistic range or implausible scores).

We will use this as a draft for a more formal quality report that documents:

- Variables’ missingness levels  
- Outliers and how they were identified  
- Decisions on whether to drop or adjust problematic records  

From here, we need to establish a consistent approach for filling in or disregarding incomplete weather information and then apply that approach to our final analysis table.

**Status:** Partially completed.



### Week 6: Pre-Analysis, Exploratory Analysis, and Automation

We started exploratory analysis with scatterplots and simple summaries linking weather to performance metrics, such as:

- Temperature vs. total points per game  
- Wind speed vs. turnovers per game  

We also created a small module to reuse loading and transformation functions across notebooks and scripts.

In addition, we began writing a single script that chains the feature extraction and integration steps so that the core pipeline can be run more easily. At this point, it is still more of a linear script than a full workflow engine, but it sets up the foundation for automation.

Next steps include:

- Extending automation to cover more of the lifecycle  
- Implementing more advanced analyses (e.g., regression models)

**Status:** In progress.



### Weeks 7–9: Pending Work

Remaining work includes:

- Finalizing cleaning and data-quality decisions  
- Running and interpreting correlation and regression models  
- Creating clearer reproducibility through setup notes, a `requirements` file, and possibly a workflow engine  
- Writing the final report and data dictionary  
- Packaging visualizations  
- Publishing a tagged final release  

**Status:** Planned.


## Updated Project Timeline and Task Progress

Below is our updated view of key tasks, their current status, and anticipated completion:

- **Lifecycle model and research questions**  
  - Status: Completed  
  - Target: Week 1  

- **Acquire CollegeFootballData games and venues**  
  - Status: Completed  
  - Target: End of Week 2  

- **Acquire Open-Meteo weather data**  
  - Status: Core functionality completed; small adjustments ongoing  
  - Target: Completed by Week 3, refinements through Week 6  

- **Determine storage model and directory structure**  
  - Status: Completed  
  - Target: End of Week 3  

- **Extract relevant football and weather features**  
  - Status: First draft completed; fine-tuning ongoing  
  - Target: Draft by Week 3, refinements by Week 6  

- **Join game and weather data**  
  - Status: Running; validation and documentation in progress  
  - Target: End of Week 6  

- **Data quality assessment and cleaning**  
  - Status: First pass completed; final remediation plan pending  
  - Target: Remediated dataset by end of Week 7  

- **Exploratory analysis and minimal visualizations**  
  - Status: Ongoing  
  - Target: Weeks 6–7  

- **Pipeline and further reproducibility metadata**  
  - Status: Script started; automation expanding  
  - Target: Weeks 7–8  

- **Regression modeling and interpretation**  
  - Status: Not started  
  - Target: Weeks 8–9  

- **Final README, requirements file, data dictionary, and final report**  
  - Status: Not started  
  - Target: Week 9 (with final tagging and release)


## Changes to the Project Plan

Since our Milestone 2 submission, we have made several changes based on instructor feedback and our assessment of the data.

### Scope Adjustments

- We limited our analysis to a more manageable subset of **recent seasons** instead of acquiring every historical season. This helps with:
  - Integration (fewer edge cases and structural changes)
  - Data quality (more consistent records)
  - API usage (fewer and more targeted requests)

- We narrowed our **main weather predictors** to:
  - Temperature  
  - Wind speed  
  - Precipitation  

Humidity and other secondary variables will still be examined descriptively but will not be treated as core predictors in the first round of modeling.

### Methodological Clarifications

- The **unit of analysis** is the **game**, not individual plays. All weather variables are aggregated to the game level, which is more compatible with our data sources and the scope of the course.
- We acknowledge that **region and performance are confounded**. Rather than treating “cold vs. warm region” as the main variable of interest, we plan to:
  - Use simple proxies for team strength (e.g., win percentage or scoring margin).  
  - Treat region as a secondary explanatory or stratification variable.

### Reproducibility and Automation

We expanded the replicability and automation aspects of the project:

- We started a pipeline script that links multiple steps together, making it easier to rerun the process from raw data to integrated tables.
- We began sketching a simple workflow diagram that will be turned into a figure for our documentation.
- Time permitting, we may adopt a more formal workflow tool, but even if we stay with Python scripts, our goal is a clear, well-documented path from raw data to analysis-ready files and visualizations.


## Individual Contributions for This Milestone

### Priyansh Modi

Priyansh’s main contributions involved **data collection, storage, and integration**:

- Implemented and refined the CollegeFootballData and Open-Meteo API scripts, including handling parameters and rate limits.
- Established the raw vs. intermediate storage layout and helped define the directory structure and file naming conventions.
- Led development of the integration script that merges game statistics with weather summaries.
- Started the pipeline script that links individual steps into a more repeatable process.

### Shivam Patel

Shivam’s main contributions involved **feature selection, validation, exploratory analysis, and documentation**:

- Wrote and refined selection scripts that determine key football variables (e.g., turnovers, total score) and weather variables (e.g., temperature, precipitation), including some derived values.
- Constructed an early version of the integrated tables and validated the joined dataset using Jupyter notebooks to check that weather values made sense for sampled games.
- Led the initial data-quality checks and drafted the written quality report.
- Started exploratory visualizations connecting weather to total scoring and turnovers per game, and drafted the written materials for this milestone.

