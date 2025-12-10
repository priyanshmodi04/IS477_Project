# Does Weather Affect College Football Scoring Across Early Season Games

## Contributors  
- Shivam Patel  
- Priyansh Modi  

## Summary  

The intention of this project is to determine whether or not weather impacts scoring in college football. Many times when people watch sports, you will hear someone say things like the weather is not helping today or it is too cold outside to score today. As they say these things from their couch, it is usually an offhand and superficial reaction based on whatever the announcers say during the game or based on trends they believe they have seen from season to season. These statements are not backed by empirical evidence. Instead, they are based on years of sports history and folklore repeated in casual conversations, debates, and social media posts. People talk about weather as if it is a major game changer, but these beliefs do not come from broad statistical evidence built up over time. They rely on the memory of that one game that was extremely snowy or that one game that was extremely hot in September.

This project is designed to take a step back, take stock of those assumptions, and test them with data. It aims to put together a clean and empirical set of weather statistics over time in relation to scoring, instead of relying on anecdotal memories of how many points were scored during that snowstorm game or that freezing night. The goal is to compile enough data over several seasons to find out if temperature really impacts scoring in a meaningful way, or if personal opinions and fan narratives have overstated its importance without people realizing it.

The project is built on a simple idea rather than complex models. It gathers the temperature at kickoff and aligns that with total points scored, and then asks whether those two variables move together in a way that actually matters.

The central research question guiding the entire project is whether there is a meaningful relationship between the temperature at which a game is played and the total points scored in that game. In order to keep this question scoped in a realistic way, games were pulled from the 2020 to 2023 seasons, but only from weeks one and two. These two weeks are useful for data collection because they cover games played across the country, from hotter southern stadiums to cooler northeastern states and many regions in between. The difference in temperature in early September is more varied than many people might think, and this creates a natural test case without having to move into midseason weather patterns and complications.

Games were collected through the CollegeFootballData application programming interface. This interface provides structured data for each game such as start times, venue names, scores, and other fields. The project then uses venue data from the same source that includes latitude and longitude. The ability to connect the location of each game to specific weather readings is critical. On the weather side, the historical archive from Open Meteo makes it possible to collect temperature, precipitation, and wind speed based on stadium coordinates and game dates. By using the start times and hourly weather readings, each game can be matched to the closest available weather observation. The final dataset becomes a cleaned and compiled table built from these two separate sources, which is then analyzed through a straightforward and transparent pipeline.

The general methodology follows a sequence of simple steps. First, collect game and venue information. Second, connect that information with hourly stadium weather drawn from coordinates and dates. Third, send requests in batches so that the weather interface is not overloaded. Fourth, merge all of this into one processed dataset. Fifth, run checks to confirm that the data looks reasonable. Finally, examine whether scoring differs in a statistically meaningful way across temperature ranges or linear trends, by looking at both summary comparisons and scatterplots with regression lines. The goal is to keep the process as simple and reproducible as possible so that each step is clear and so that findings are based on straightforward evidence rather than heavily tuned models.

One reason this project is worth doing is that college football is a very emotional environment, and weather stories build quickly. For example, fans almost always remember a rare game with heavy snow, strong rain, or extreme heat and treat that single game as if it reflects how weather usually affects play. However, a single game is not a reliable data source, and people remember surprising events much more than ordinary ones. This project takes the opposite approach.

Instead of focusing on highlight moments or extreme weather games, it looks at normal games in their normal ranges of conditions. It evaluates what happens across many games, rather than relying on stories that spread through social media or sports talk shows.

This project also shows how accessible sports analytics can be. Anyone with access to public interfaces and a clear workflow could carry out a similar analysis. By building and organizing a structured pipeline, the project shows how data science can turn vague thoughts into something measurable. For example, ideas like warmer weather makes the game more open, or cold weather slows offenses down, can be tested directly instead of just repeated. The project shows that many of these common claims do not show a strong cumulative effect, at least not in early season matchups.

The results lead to clear findings, especially for scoring. Scoring appears fairly consistent across temperature bins, and the average points in very cold, cold, mild, and hot conditions are similar. The regression line between temperature and total points is almost flat. For this dataset, temperature does not play a meaningful role in scoring.

This conclusion is valuable by itself. It suggests that temperature does not matter as much as many people think and gives a more realistic sense of what actually affects scoring. Coaches, analysts, and betting groups often treat weather forecasts as if they are major inputs, but this work points toward a more grounded view. It suggests that scoring comes more from strategy, player talent, and team strengths on that particular day than from a small change in temperature.

This project also shows how weather statistics can be consistently produced even if the resulting relationship is weak. A weaker relationship still demonstrates that the data pipeline is strong and repeatable. It also allows future seasons to be added and compared later on. In that way, simple ideas can be examined through a careful and data driven process instead of through speculation.

## Data Profile  

The two primary data sources in this project are college football game results combined with game information, including venue location, and hour by hour weather trends from the Open Meteo interface. Making these two sources work together requires significant structural alignment because they are designed for different purposes. Sports data is organized around discrete events such as games, teams, and scores. Meteorological data is organized around regular time intervals such as hourly readings and is tied tightly to geography.

The game data comes from the CollegeFootballData interface through a games endpoint, which is called for every relevant season and week. Since the project focuses on the 2020 through 2023 seasons and limits analysis to weeks one and two of each year, this endpoint is used to pull game identifiers, seasons, weeks, start times, venue names, home and away teams, and final scores. This information is necessary to know who played, when they played, where they played, and what the scoring outcome was, so that weather can later be matched to the game.

The code that handles this step is located in the data file named data dot py. This script sends the calls to the interface, collects the responses, and organizes them into data frames for further use. Venue data, which is also provided by the same interface, is accessed through a separate venues endpoint. This venue data contains latitude and longitude for stadiums and enables the link between games and weather readings.

In some cases, stadiums are written differently between endpoints or change names when sponsors change. To deal with these inconsistencies, venue names are cleaned and standardized so that the game table and venue table match correctly. This is an important step because a mismatch here would cause the weather matching to break, since it depends on accurate coordinates for each stadium.

The weather data comes from the Open Meteo historical archive. This interface provides hourly temperature in degrees, precipitation in millimeters, and wind speed in meters per second. For each stadium and game date combination, one full day of hourly weather readings is requested. In some cases, multiple games may be played at the same stadium within the timeframe of interest. To avoid repeated calls for the same location and date, the results are cached. The cache is keyed by latitude, longitude, and date so that once a set of hourly readings is retrieved, it can be reused for any game at that stadium on that same day.

This caching approach prevents unnecessary repeated requests and avoids overloading the weather interface. It also speeds up repeated runs of the pipeline, since some of the work does not need to be done again. After the weather for a location and date is loaded, the hour closest to the kickoff time is selected and treated as the weather at kickoff.

Aligning sports data and weather data can be difficult because of the differences in structure and purpose. Sports tables focus on categories such as home team, away team, and final score. Weather tables focus on continuous measurements and geographic coordinates. Connecting the two requires solving time zone issues, matching timestamps, handling different formats, and carefully interpreting coordinate precision.

Hourly weather was chosen on purpose. Some services provide higher frequency data, but minute level readings are often noisy or interpolated estimates. Hourly readings, on the other hand, are accurate enough to reflect real field conditions while also being stable. This suits the goal of a reliable and repeatable analysis. It reflects what players and coaches actually experience more closely than hyper granular readings that may not add meaningful insight.

The end result of all preprocessing is a final dataset saved as games underscore with underscore weather dot csv in the data processed folder. This file contains all of the game fields described earlier, as well as stadium latitude and longitude, temperature at kickoff, precipitation level, wind speed, home score, away score, and a total points field that combines the two scores.

A Snakefile governs the entire workflow. It calls data dot py to build the combined game and weather dataset, quality dot py to assess data quality, analysis dot py to run scoring analyses, and checksums dot py to verify file integrity through checksum records. Each step produces files in the data raw, data processed, and results folders. This separation makes the pipeline easy to follow and makes it possible to see how the final outputs are produced from raw sources.

One additional feature was created named total points. This simply adds home points and away points together. For analytical purposes, another variable was created to bin temperature into four categories described as very cold, cold, mild, and hot. Weather is aligned using latitude, longitude, date, and adjusted kickoff time. If any of these pieces are missing or inaccurate, meaningful weather cannot be attached and those games remain without weather information. Kickoff time was adjusted to align with the nearest hour so that hourly weather could be matched.

One thing that stands out when looking at the data profile is the large number of stadiums used in college football, even in just the first two weeks of the season. Games are played in southern states with high humidity, northern states with cooler temperatures, western states with dry air and different temperature ranges, higher altitude stadiums, and coastal stadiums. This geographic diversity means that even within two weeks, there is a wide variety of weather conditions. That diversity increases the strength of the dataset and reduces the risk of studying only a narrow climate.

In an ideal extension of this work, extra stadium metadata would be included such as capacity, whether the stadium is covered or open, and the altitude above sea level. Weather interacts differently with covered stadiums compared to open air ones. Altitude can affect air density, which may influence kicking and deep passing. Although these attributes are not included in this version of the project, they are promising areas for future expansion.

All of the data is publicly available and does not contain sensitive information. There are no personal identifiers for players or staff. The work follows academic standards and both interfaces used here allow for academic and non commercial use, which matches the nature of this project.

## Data Quality  

To assess the quality of the final dataset, the script quality dot py loads the processed file into Python, counts missing values for key fields, and produces summary statistics for numerical columns. Based on this assessment, the number of games included in the file matches expectations for weeks one and two of the selected seasons.

Ideally, most fields in the table would be complete. In practice, some games are missing temperature or wind speed values. This typically occurs either because the CollegeFootballData interface does not provide coordinates for that stadium or because the Open Meteo archive does not have complete weather records for that location and date. A stadium without latitude and longitude cannot be mapped to weather. Likewise, if a location and date combination fails to return hourly data, the game tied to that record will not have temperature or wind values.

There were no serious issues with duplication in the final dataset. The main technical work in this area involved converting timestamps into a consistent and usable format. The games endpoint returns times with time zone information and offset details. These had to be standardized into a format suitable for weather queries. Once this was done, the hourly weather lookups became more reliable and the match rate for weather readings improved.

Missing values were left unchanged in the processed dataset. During analysis, games with missing temperature were excluded because the research question depends on temperature. Attempting to estimate temperature for missing entries would introduce bias and would weaken the integrity of the conclusions, so exclusion was the more honest and straightforward choice.

The quality checks showed that total points align with realistic college football scores. There were no games with extremely low or unrealistically high totals. This supports the idea that the scoring data is accurate. Temperature values also match expectations based on stadium location and time of year. Southern stadiums tend to have mild to warm temperatures in early September and northern stadiums sometimes show cooler readings.

Overall, the dataset highlights how real world data almost never behaves perfectly. It is rare to find fully complete and perfectly consistent data. Interfaces can have gaps, naming conventions can vary, and some fields may be missing. This project shows that even widely used sports data sources can have holes, especially around location data. Part of the work in any real data project is to acknowledge these imperfections, document them, and adjust the analysis accordingly.

Another important aspect of data quality involves precision. Even though Open Meteo provides accurate hourly readings, the exact temperature at kickoff might differ slightly from the reading at the closest hour. This can happen around times of rapid cooling, such as around sunset. These differences are usually small but are worth recognizing. Because the project focuses on general trends rather than tiny fluctuations, this level of precision is acceptable. However, it is still a limitation that should be kept in mind when interpreting results.

Finally, quality dot py helps validate the integrity of the pipeline. It confirms that total points match the sum of home and away scores and it checks that numeric conversions and saving operations function properly. This matters because the workflow involves multiple scripts and an automated tool, so having a validation step reduces the risk of hidden errors.

The primary limitation of the dataset is that it only covers weeks one and two in the four selected seasons. However, within that scope, the cleaned data is strong enough to support the main research question.

## How It Was Analyzed  

To analyze the compiled dataset, the script analysis dot py carries out two main analyses that are aligned with the simplicity of the research question.

The first analysis divides games into four temperature categories. These categories correspond to less than five degrees Celsius, between five and fifteen degrees, between fifteen and twenty five degrees, and greater than twenty five degrees. For each category, the script calculates the average total points scored. These averages are then compared across categories. The results show that the averages are very close to each other. This suggests that even at cooler or warmer edges of the early season, average scoring does not change much. A bar chart displays these averages side by side, and visually the bars look similar in height. This makes it easy to see that temperature changes within this range do not strongly affect scoring.

The second analysis plots each game as a point in a scatterplot, with temperature on the horizontal axis and total points on the vertical axis. A simple linear regression line is then fit to the data. The slope of this line is very small, which means temperature has almost no linear relationship with total points scored. The points are scattered across the plot without forming a distinct upward or downward pattern. This reinforces the idea that scoring is driven by many factors other than temperature.

Another way to look at the analysis is to ask why temperature might not have much effect. At first, it seems logical that extreme cold or heat would affect players, but football is a highly structured sport. There are frequent stoppages, timeouts, and substitutions. Players are usually only on the field for short bursts of time followed by breaks. This allows them to recover and adjust to conditions more easily than athletes in continuous endurance sports. That structure might reduce the impact of weather and create more resilience to temperature changes.

Teams also adjust their strategies when conditions are unusual. In hot weather, there is often more rotation of players and more emphasis on hydration. In cold weather, coaches may choose safer play calls to avoid mistakes. These adjustments help balance out the effects that weather might otherwise have. What fans sometimes describe as the weather ruining the offense could actually be a combination of playcalling, opponent strategies, and execution, which all interact with weather in complex ways.

Offensive styles also differ widely from team to team. Some teams rely on fast paced passing attacks. Others build their identity around a strong running game or a balanced approach. Because of this variety, temperature may affect certain teams differently than others. When results are averaged across many teams and games, the individual effects can cancel out. This is another reason why the overall relationship between temperature and scoring appears weak in the early season.

Taken together, the analyses suggest that scoring is relatively stable across the range of temperatures observed in early season games. Temperature does not appear to have a strong predictive relationship with total points. Other factors, such as team quality, coaching, matchups, and in game events, likely have a much larger effect on how many points are scored.

## Improvements for Future Work  

There are several ways this study could be improved or expanded if it were to continue. One clear step would be to extend the dataset beyond weeks one and two. Including later weeks of the season would introduce colder late autumn and early winter games, especially in northern stadiums. Those conditions might create more extreme weather effects that are not captured in early September.

Another improvement would involve adding more weather related variables. In addition to temperature, the project could consider humidity, barometric pressure, visibility, and derived measures such as heat index and wind chill. These measures capture how the weather actually feels to players, coaches, and fans, and can influence fatigue and performance differently than temperature alone. For example, two games at the same temperature could feel very different depending on humidity levels.

The modeling approach could also be expanded. The present analysis uses simple averages and linear regression. While this is appropriate for a first pass, more advanced models such as decision trees or random forests could uncover subtle non linear patterns or interactions between weather and game context. There may be threshold effects where scoring changes more noticeably beyond a certain level of cold or heat. Identifying such thresholds would require more data and more complex modeling.

Documentation and pipeline transparency could be improved as well. Although the current workflow is organized and reproducible, adding more comments, visual diagrams, and intermediate summaries would make it easier for others to follow and reuse the pipeline. This is especially useful if more datasets, features, or analysis steps are added in the future.

Future work could also look at changes within a game rather than just full game summaries. For example, it would be interesting to see if scoring drops in the second half when temperatures fall rapidly or whether passing becomes less effective during certain parts of the day. These types of temporal patterns would require a more detailed play by play or drive level dataset, but they could reveal subtle weather impacts that are not visible in total game scores.

Another promising direction is to add team level and player level context. Some teams might be more sensitive to weather than others, especially those that depend heavily on the passing game. Experienced quarterbacks might perform consistently across a wider range of conditions, while younger quarterbacks might struggle more in cold or windy weather. Incorporating these factors would allow the analysis to move beyond overall averages and examine how the effects of weather vary across different styles of play and different types of teams.

Ultimately, this project works as a proof of concept. It shows how a clear question, a couple of public interfaces, and a simple pipeline can be combined to test a popular belief in sports. It also shows that the real world rarely behaves as neatly as our stories about it. By building a clean process from data collection through analysis, the project lays a foundation that can be extended and adapted in future work.

## Reproducing  

To reproduce the results from this project, the full workflow can be run directly from the project repository. First, clone the repository and move into the project directory:
git clone https://github.com/priyanshmodi04/IS477_Project.git
cd IS477_Project
Next, create and activate a virtual environment:
python -m venv venv
source venv/bin/activate
Then install all required dependencies:
pip install -r requirements.txt
The final processed dataset used for the analyses is stored externally. Download the file named games_with_weather.csv from the following Box link:
https://uofi.box.com/s/gr5alqmyc0h8jevwwckdlxw9j8dz79z8
Place this file into the following folder path inside the project:
data/processed/games_with_weather.csv
Once the data is in the right location and the environment is set up, the entire workflow can be run with:
./run_all.sh
This script uses the Snakefile to coordinate the steps. It will rebuild the processed dataset if needed, run data quality checks, perform the analysis, generate figures, and write outputs into the results/ directory. These outputs include the data quality summary, the temperature-bin statistics, the bar plot, the regression plot, and the checksum file that records data integrity for key files.
Anyone who wants to fully reproduce the project from raw APIs (rather than using the Box file) will need to set a valid CollegeFootballData API key in their environment. Without a working API key, the data acquisition step that pulls games and venues from CollegeFootballData cannot be run successfully. The Open-Meteo API does not require authentication and can be called without a key.
Running these steps end-to-end will recreate the full workflow and produce all of the results described in this report.

## References

CollegeFootballData API – used to collect college football game schedules, scores, and venue information for the 2020–2023 seasons.
Open-Meteo Archive API – used to retrieve historical hourly temperature, precipitation, and wind speed data matched to game locations and dates.
Python libraries such as pandas, numpy, matplotlib, requests, and tqdm – used for data retrieval, cleaning, computation, and visualization.
Snakemake – used to define and run the workflow that connects data acquisition, processing, quality checks, and analysis into a single reproducible pipeline.
All data used in this project is publicly accessible and non-sensitive, with no personally identifiable or player-specific information included.



