# snakefile

# final targets
rule all:
    input:
        "data/processed/games_with_weather.csv",
        "results/data_quality_summary.csv",
        "results/points_vs_temp.png",
        "results/points_vs_temp_stats.csv",
        "results/temp_vs_points_regression.png"


# build the integrated games + weather dataset
rule build_dataset:
    output:
        "data/processed/games_with_weather.csv"
    shell:
        "python code/data.py"


# run basic data quality checks
rule data_quality:
    input:
        "data/processed/games_with_weather.csv"
    output:
        "results/data_quality_summary.csv"
    shell:
        "python code/quality.py"


# run analysis and create plots
rule analysis:
    input:
        "data/processed/games_with_weather.csv"
    output:
        "results/points_vs_temp.png",
        "results/points_vs_temp_stats.csv",
        "results/temp_vs_points_regression.png"
    shell:
        "python code/analysis.py"