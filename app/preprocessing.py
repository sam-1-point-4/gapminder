import pandas as pd
import numpy as np
import time
import streamlit as st

@st.cache_data
def load_and_preprocess_data():
    # Load CSV files
    life_exp = pd.read_csv('src/lex.csv')
    population = pd.read_csv('src/pop.csv')
    gni = pd.read_csv('src/gni.csv')

    # Forward fill missing values by country
    life_exp = life_exp.sort_values(['country', 'year'])
    life_exp = life_exp.groupby('country').ffill()

    population = population.sort_values(['country', 'year'])
    population = population.groupby('country').ffill()

    gni = gni.sort_values(['country', 'year'])
    gni = gni.groupby('country').ffill()

    # Tidy data: melt so columns are country, year, KPI
    life_exp_tidy = life_exp.melt(id_vars=['country'], var_name='year', value_name='life_expectancy')
    life_exp_tidy['year'] = life_exp_tidy['year'].astype(int)

    population_tidy = population.melt(id_vars=['country'], var_name='year', value_name='population')
    population_tidy['year'] = population_tidy['year'].astype(int)

    gni_tidy = gni.melt(id_vars=['country'], var_name='year', value_name='gni_per_capita')
    gni_tidy['year'] = gni_tidy['year'].astype(int)

    # Merge all three dataframes
    df = life_exp_tidy.merge(population_tidy, on=['country', 'year'])
    df = df.merge(gni_tidy, on=['country', 'year'])

    return df