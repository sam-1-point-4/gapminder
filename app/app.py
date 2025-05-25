import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from preprocessing import load_and_preprocess_data  # Import the function

df = load_and_preprocess_data()  # Use the DataFrame from preprocessing.py

st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Education")

# Year slider with animation (Streamlit 1.18+)
year = st.slider(
    "Select Year",
    min_value=int(df['year'].min()),
    max_value=int(df['year'].max()),
    value=2025,
    step=1,
    key="year"
)

countries = df['country'].unique().tolist()

selected_countries = st.multiselect(
    "Select Countries",
    options=countries,
    default=['Germany'],
    key="countries"
)

filtered_df = df[df['country'].isin(selected_countries)]

# Set constant x-axis range for comparability
gni_min = df['gni_per_capita'].min()
gni_max = df['gni_per_capita'].max()

# Bubble chart with animation
fig = px.scatter(
    df[df['country'].isin(selected_countries)],
    x="gni_per_capita",
    y="life_expectancy",
    size="population",
    color="country",
    hover_name="country",
    animation_frame="year",
    animation_group="country",
    log_x=True,
    size_max=60,
    range_x=[gni_min, gni_max],
    range_y=[df['life_expectancy'].min(), df['life_expectancy'].max()],
    labels={
        "gni_per_capita": "GNI per Capita (log scale, PPP $)",
        "life_expectancy": "Life Expectancy",
        "population": "Population"
    },
    title="Gapminder Bubble Chart"
)

fig.update_layout(transition={'duration': 500})
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500

st.plotly_chart(fig, use_container_width=True)
