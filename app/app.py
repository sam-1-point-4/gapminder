import streamlit as st
import plotly.express as px
from preprocessing import load_preprocessed_data

# Load and preprocess data
df = load_preprocessed_data()

st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Education")

# Widgets
years = sorted(df['year'].unique())
countries = sorted(df['country'].unique())

# Initialize session state for animation
if 'year' not in st.session_state:
    st.session_state['year'] = years[0]
if 'is_animating' not in st.session_state:
    st.session_state['is_animating'] = False

def set_year():
    st.session_state['year'] = st.session_state['selected_year']

selected_year = st.slider(
    "Select Year",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=int(st.session_state['year']),
    step=1,
    format="%d",
    key='selected_year',
    on_change=set_year
)

default_country = ['India'] if 'India' in countries else [countries[0]] if countries else []

selected_countries = st.multiselect(
    "Select Countries",
    options=countries,
    default=default_country
)

gni_min = df['gni_per_capita_ppp'].min()
gni_max = df['gni_per_capita_ppp'].max()
life_min = df['life_expectancy'].min()
life_max = df['life_expectancy'].max()

def plot_chart(year, countries):
    filtered_df = df[df['year'] == year]
    # Only filter by countries if at least one country is selected
    if countries:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    # Remove rows with NaN in 'population'
    filtered_df = filtered_df.dropna(subset=['population'])
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        return
    fig = px.scatter(
        filtered_df,
        x="gni_per_capita_ppp",
        y="life_expectancy",
        size="population",
        color="country",
        hover_name="country",
        log_x=True,
        size_max=60,
        range_x=[gni_min, gni_max],
        range_y=[life_min, life_max],
        labels={
            "gni_per_capita_ppp": "GNI per Capita (log scale, PPP $)",
            "life_expectancy": "Life Expectancy",
            "population": "Population"
        },
    )
    fig.update_layout(title=f"Gapminder Bubble Chart - {year}")
    st.plotly_chart(fig, use_container_width=True)

# Animation controls
col1, col2 = st.columns([1, 8])
with col1:
    if st.button("▶️ Play Animation"):
        st.session_state['is_animating'] = True

with col2:
    pass  

import time

if st.session_state['is_animating']:
    current_index = years.index(st.session_state['year'])
    if current_index < len(years) - 1:
        next_year = years[current_index + 1]
        st.session_state['year'] = next_year
        plot_chart(next_year, selected_countries)
        time.sleep(0.4)
        st.experimental_rerun()
    else:
        st.session_state['is_animating'] = False
        plot_chart(st.session_state['year'], selected_countries)
else:
    plot_chart(st.session_state['year'], selected_countries)
