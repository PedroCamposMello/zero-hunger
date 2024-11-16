import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='🎲'
)

# ======= Dashboard =======

# ------- Sidebar -------

image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Zero Hunger')
st.sidebar.markdown('## All Cuisines Are Yours!')

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powerd by PedroMello')

# ------- Page -------

st.write('# Zero Hunger Management Dashboard')

st.markdown(
    '''
    Management Dashboard was built to monitor the growth metrics for a restaurant agregator app.
    ### How to use the Management Dashboard:
    - Overiew: General metrics for restaurants.
    - Countries View: Restaurants metrics based on countries
    - Cities View: Restaurants metrics based on cities
    - Cuisines View: Restaurants metrics based on each cuisines types
    ### Ask for help:
        - @pedromello
    '''
)