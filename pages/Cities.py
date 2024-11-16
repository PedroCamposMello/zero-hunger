# ======= Importations =======

# Importação de bibliotecas basicas necessárias:
import pandas as pd
import numpy as np

import streamlit as st

import inflection

import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

# Configuração da página:

st.set_page_config(
    page_title='Countries View',
    page_icon='🏙',
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

st.header('Cities View')

# Layout

# Auxiliary dataframe
columns_select = ['city', 'country']
df_city = df.loc[:, columns_select].drop_duplicates().reset_index(drop=True)

with st.container():
    st.markdown('#### Top 10 cities with highest count of restaurants')

    columns_select = ['restaurant_id', 'city']
    rows_group = ['city']
    df_aux = df.loc[:, columns_select].groupby(rows_group).count().head(10).sort_values(by='restaurant_id', ascending=False).reset_index()

    df_aux = df_aux.join(df_city.set_index('city'), on='city')

    df_aux.columns = ['City', 'Restaurants' , 'Country']

    fig = px.bar(df_aux, x='City', 
       y='Restaurants', 
       color='Country', 
       color_discrete_sequence=px.colors.qualitative.G10,
       )

    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Top cities with highest restaurants average rating')

        columns_select = ['aggregate_rating', 'city']
        rows_group = ['city']
        rows_filter = df['aggregate_rating'] != 0
        head_range = 10

        df_aux = df.loc[rows_filter, columns_select].groupby(rows_group).mean().round(2).sort_values(by='aggregate_rating', ascending=False).reset_index().head(head_range)

        df_aux = df_aux.join(df_city.set_index('city'), on='city')

        df_aux.columns = ['City', 'Ratting', 'Country']

        fig = px.bar(
                    df_aux, 
                    x='City', 
                    y='Ratting', 
                    color='Country',
                    color_discrete_sequence=px.colors.qualitative.G10
                    )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('#### Top cities with lowest restaurants average rating')

        columns_select = ['aggregate_rating', 'city']
        rows_group = ['city']
        rows_filter = df['aggregate_rating'] != 0
        head_range = 10

        df_aux = df.loc[rows_filter, columns_select].groupby(rows_group).mean().round(2).sort_values(by='aggregate_rating', ascending=True).reset_index().head(head_range)

        df_aux = df_aux.join(df_city.set_index('city'), on='city')

        df_aux.columns = ['City', 'Ratting', 'Country']

        fig = px.bar(
                    df_aux, 
                    x='City', 
                    y='Ratting', 
                    color='Country', 
                    color_discrete_sequence=px.colors.qualitative.G10
                    )

        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown('#### Top cities with most cuisines types')

    columns_select = ['cuisines', 'city']
    rows_group = ['city']
    head_range = 10

    df_aux = df.loc[:, columns_select].groupby(rows_group).nunique().sort_values(by='cuisines', ascending=False).reset_index().head(head_range)

    df_aux = df_aux.join(df_city.set_index('city'), on='city')

    df_aux.columns = ['City', 'Cuisines', 'Country']

    fig = px.bar(
                df_aux, 
                x='City', 
                y='Cuisines', 
                color='Country', 
                color_discrete_sequence=px.colors.qualitative.G10
                )

    st.plotly_chart(fig, use_container_width=True)