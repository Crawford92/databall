import pandas as pd
import plotly.express as px
import nflreadpy as nfl
import math
import seaborn as sns
import matplotlib.pyplot as plt
import polars as pl

 

henry_id = "00-0032764"
pbp = nfl.load_pbp([2019, 2020, 2021, 2022, 2023, 2024])
sched = nfl.load_schedules([2019, 2020, 2021, 2022, 2023, 2024])

# join on temperature
pbp = pbp.join(
    sched.select(['game_id','temp']),
    on='game_id',
    how='left'
)

# filter Derrick Henry rushes
henry_plays = pbp.filter(
    (pbp['rusher_id'] == henry_id) &
    (pbp['play_type'] == 'run') &
    (pbp['temp'].is_not_null())     # drop if no temp, like indoor, or no data available. 
)
 

# groupby each game he played
per_game = henry_plays.group_by("game_id").agg([
    pl.col("yards_gained").mean().alias("avg_yards"),
    pl.col("temp").mean().alias("game_temp"),
    pl.len().alias("attempts")
]).to_pandas()


fig = px.scatter(
    per_game,
    x="game_temp",
    y="avg_yards",
    size="attempts",   # bigger dot = more carries
    trendline="ols",
    title="Derrick Henry Avg Yards per Game vs Temperature (2019–2024)",
    labels={"game_temp":"Temperature (°F)", "avg_yards":"Avg Yards per Carry"}
)

fig.write_html("henry_scatter.html", auto_open=True)


 