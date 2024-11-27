import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

# Data Frame
overall_detail_df= pd.read_csv('India.csv')
states_df = pd.read_csv("Latitude and Longitude State wise centroids 2020.csv")
list_of_states = overall_detail_df['State'].unique().tolist()
list_of_states.insert(0, 'Overall India')

st.sidebar.title('Explore India Census Insights')
selected_state = st.sidebar.selectbox('Select a State', list_of_states)
primary = st.sidebar.selectbox('Select Primary Parameter', sorted(overall_detail_df.columns[5:]))
secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(overall_detail_df.columns[5:]))

plot = st.sidebar.button('Plot Graph')

if plot:
    if selected_state == 'Overall India':
        fig = px.scatter_mapbox(overall_detail_df, lat="Latitude", lon="Longitude", size=primary, color=secondary,
                                color_continuous_scale='Viridis',  # Change the color scale here
                                size_max=25, zoom=6, mapbox_style="carto-positron",
                                width=1200, height=700, hover_name='District')
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Plot for Selected State
        state_df = overall_detail_df[overall_detail_df['State'] == selected_state]
        fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude", size=primary, color=secondary,
                                color_continuous_scale='Viridis',  # Change the color scale here
                                size_max=25, zoom=6, mapbox_style="carto-positron",
                                width=1200, height=700, hover_name='District')
        st.plotly_chart(fig, use_container_width=True)
