# ======= Importations =======

# Importação de bibliotecas basicas necessárias:
import pandas as pd
import numpy as np

import streamlit as st

import inflection

import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

# Configuração da página:

st.set_page_config(
    page_title='Overview',
    page_icon='📈',
    layout='wide'
)

# Importing data creatig a safety copy of the dataframe
path = 'data\zomato.csv'
df_0 = pd.read_csv(path, sep=',', decimal='.')
df = df_0.copy()

# ======= Functions =======

# Country naming

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]

# Price categorization

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Color naming

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]

# Column renaming

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# ======= Data wrangling =======

# Column renaming:
df = rename_columns(df)

# Changing the 'country_code' column to 'country' column:
df['country_code'] = df['country_code'].apply(country_name)
df.rename(columns={'country_code' : 'country'}, inplace=True)

# Changing the 'price_range' column to a textual category:
df['price_range'] = df['price_range'].apply(create_price_type)

# Changing the 'rating_color' column to a textual category:
df['rating_color'] = df['rating_color'].apply(color_name)

# Simplificating the 'cusines' column to just one type of cusine per register:
df['cuisines'] = df.loc[:, "cuisines"].apply(lambda x: str(x).split(",")[0])

# Removing duplicated rows:
df = df.drop_duplicates()

# ======= Dashboard =======

# ------- Sidebar -------

image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Zero Hunger')
st.sidebar.markdown('## All Cuisines Are Yours!')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Filters')

# Country filter

country_list = list(df['country'].unique())
country_filter = st.sidebar.multiselect(
    'Select countries',
    country_list,
    default=country_list
)

rows_filter = df['country'].isin(country_filter)
df = df.loc[rows_filter, :]

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powerd by PedroMello')

# ------- Page -------

# Header

st.header('Overview')

# Layout

with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_variable = df['restaurant_id'].nunique()
        col1.metric('Registered restaurants', metric_variable)
    
    with col2:
        metric_variable = df.loc[(df['has_online_delivery'] == 1), 'restaurant_id'].nunique()
        col2.metric('Restaurants which have online delivery', metric_variable)

    with col3:
        metric_variable = df['country'].nunique()
        col3.metric('Registered countries', metric_variable)

    with col4:
        metric_variable = df['cuisines'].nunique()
        col4.metric('Registered cuisines', metric_variable)

with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_variable = df.loc[(df['has_table_booking'] == 1), 'restaurant_id'].nunique()
        col1.metric('Restaurants which have table booking', metric_variable)
    
    with col2:
        metric_variable = df.loc[(df['has_online_delivery'] == 1) & (df['is_delivering_now'] == 1), 'restaurant_id'].nunique()
        col2.metric('Restaurants which have delivery services', metric_variable)

    with col3:
        metric_variable = df['city'].nunique()
        col3.metric('Registered cities', metric_variable)

    with col4:
        metric_variable = df.loc[:, 'votes'].sum()
        col4.metric('Number of reviews', metric_variable)

with st.container():
    # Creating map's dataframe:
    columns_select = ['restaurant_id', 'restaurant_name', 'latitude', 'longitude', 'rating_color']
    data_plot = df.loc[:, columns_select].drop_duplicates()

    # Creating map:
    map = folium.Map(
                    location=[ data_plot['latitude'].mean(), data_plot['longitude'].mean() ],
                    zoom_start=2,
                    zoom_scale=True
                    )

    # Add MapCluster to map:
    cluster = MarkerCluster(maxClusterRadius=50).add_to(map)

    # Creating markers:
    for index, location_info in data_plot.iterrows():
        folium.Marker(
            [location_info['latitude'], location_info['longitude']],
            popup = location_info['restaurant_name'],
            icon=folium.Icon(color=location_info['rating_color'], icon="cutlery", prefix="fa")
            ).add_to(cluster)

    folium_static(map, width=1300)

