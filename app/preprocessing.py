import os
import pandas as pd
import streamlit as st

SRC_DIR = os.path.join(os.path.dirname(__file__), 'src')

def parse_population(val):
    if pd.isna(val):
        return None
    val = str(val).strip()
    if val.endswith('M'):
        try:
            return float(val[:-1]) * 1_000_000
        except ValueError:
            return None
    if val.endswith('K'):
        try:
            return float(val[:-1]) * 1_000
        except ValueError:
            return None
    try:
        return float(val)
    except ValueError:
        return None

def load_and_tidy_csv(filename, value_name, parse_func=None):
    df = pd.read_csv(os.path.join(SRC_DIR, filename))
    year_cols = [col for col in df.columns if col.lower() != 'country']
    df = df.sort_values('country')
    df[year_cols] = df.groupby('country')[year_cols].ffill()
    tidy = df.melt(id_vars='country', value_vars=year_cols,
                   var_name='year', value_name=value_name)
    tidy['year'] = tidy['year'].astype(str)
    if parse_func:
        tidy[value_name] = tidy[value_name].apply(parse_func)
    return tidy

@st.cache_data
def load_preprocessed_data():
    life_expectancy = load_and_tidy_csv('lex.csv', 'life_expectancy')
    population = load_and_tidy_csv('pop.csv', 'population', parse_population)
    gni = load_and_tidy_csv('gni.csv', 'gni_per_capita_ppp')

    df = life_expectancy.merge(population, on=['country', 'year'], how='outer')
    df = df.merge(gni, on=['country', 'year'], how='outer')

    df['year'] = df['year'].astype(int)
    df['life_expectancy'] = pd.to_numeric(df['life_expectancy'], errors='coerce')
    df['population'] = pd.to_numeric(df['population'], errors='coerce')
    df['gni_per_capita_ppp'] = pd.to_numeric(df['gni_per_capita_ppp'], errors='coerce')

    df = df.sort_values(['country', 'year'])
    df[['life_expectancy', 'population', 'gni_per_capita_ppp']] = (
        df.groupby('country')[['life_expectancy', 'population', 'gni_per_capita_ppp']].ffill()
    )

    df = df[df['population'].notna() & (df['population'] > 0)]

    return df