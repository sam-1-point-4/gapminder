import streamlit as st
import pandas as pd
import time

st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Education")

st.slider(
        "Select Year",
        min_value=1900,
        max_value=2099,
        value=2025,
        key="year",
        step=1
    )

st.write("You selected:", st.session_state.year)

countries = ['United States', 'India', 'China', 'Brazil', 'Germany', 'South Africa', 
             'Australia', 'Canada', 'France', 'Italy', 'Spain', 'United Kingdom', 
             'Japan', 'Ukraine' 'Mexico', 'Argentina', 'Turkey', 'Netherlands',
             'Sweden', 'Norway', 'Finland', 'Denmark', 'Belgium', 'Switzerland','Egypt']
selected_countries = st.multiselect(
    "Select Countries",
    options=countries,
    default=['Germany'],
    key="countries"
)
