import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
final_df = pd.read_csv('India.csv')
state_df = pd.read_csv('Latitude and Longitude State wise centroids 2020.csv')

def overall(state, Primary_level, Secondary_level):
    """
    Displays a map showing the relationship between two educational levels for a given state or for all of India.

    Parameters:
    - state (str): The state to analyze. If 'Overall India', shows data for the entire country.
    - Primary_level (str): The primary education level (used to set bubble sizes).
    - Secondary_level (str): The secondary education level (used to set bubble color).
    """
    final_df["State_District"] = final_df["State"] + " --- " + final_df["District"]
    if state == 'Overall India':
        title_text = f"{state} Analysis of {Primary_level} vs {Secondary_level}"
        fig = px.scatter_mapbox(final_df, lat="Latitude", lon="Longitude", size=Primary_level, color=Secondary_level,
                                color_continuous_scale='Viridis', size_max=25, zoom=3, mapbox_style="carto-positron",
                                width=1200, height=700, hover_name='State_District',
                                hover_data={'State': False, 'Latitude': False, 'Longitude': False},
                                title=title_text)
        fig.update_layout(title={'x': 0.34})
        st.plotly_chart(fig, use_container_width=True)
    else:
        state_detail = final_df[final_df['State'] == state]
        title_text = f"{state} Analysis of {Primary_level} vs {Secondary_level}"
        fig = px.scatter_mapbox(state_detail, lat="Latitude", lon="Longitude", size=Primary_level, color=Secondary_level,
                                color_continuous_scale='Viridis', size_max=20, zoom=3, mapbox_style="carto-positron",
                                width=1200, height=700, hover_name='State_District',
                                hover_data={'State': False, 'Latitude': False, 'Longitude': False},
                                title=title_text)
        fig.update_layout(title={'x': 0.34})
        st.plotly_chart(fig, use_container_width=True)


def district_category(State, category,top_bottom, num_districts):
    """
    Displays a map of the top 5 districts in a specified state based on a selected category.

    Parameters:
    - State (str): The state to analyze.
    - category (str): The category to rank districts by.
    - top_bottom(str): To get district from  top or bottom
    - num_districts(int): To get number of districts
    """
    top5 = final_df[final_df['State'] == State].sort_values(by=category, ascending=(top_bottom =='Bottom')).head(num_districts)
    fig = px.scatter_mapbox(
        top5, lat="Latitude", lon="Longitude", size=category, color=category,
        color_continuous_scale='Viridis', size_max=20, zoom=6, mapbox_style="carto-positron",
        width=1200, height=700, hover_name='District',
        hover_data={'State': True, 'Latitude': False, 'Longitude': False}
    )
    fig.update_layout(title=f"Top 5 Districts in {State} by {category}", title_x=0.34)
    st.plotly_chart(fig, use_container_width=True)


def plot_state_on_map(state_name):
    """
    Displays a map of districts in the specified state with bubble sizes based on population.

    Parameters:
    - state_name (str): The name of the state to plot.
    """
    selected_state_df = final_df[final_df['State'] == state_name]
    fig = px.scatter_mapbox(
        selected_state_df, lat="Latitude", lon="Longitude", hover_name="District",
        size="Population", zoom=4, size_max=20, mapbox_style="carto-positron",
        width=1200, height=700, hover_data={'State': True, 'Latitude': False, 'Longitude': False}
    )
    fig.update_layout(
        mapbox_center={"lat": selected_state_df.iloc[0]['Latitude'],
                       "lon": selected_state_df.iloc[0]['Longitude']},
        mapbox_zoom=5, title=f"Map of Districts in {state_name}", title_x=0.34
    )
    st.plotly_chart(fig, use_container_width=True)


def state_District_information(state, district, category):
    """
    Displays a map showing information for a specific district in a specified state based on a chosen category.

    Parameters:
    - state (str): The state to analyze.
    - district (str): The district within the state.
    - category (str): The category to use for color and bubble size.
    """
    state_df = final_df[(final_df['State'] == state) & (final_df['District'] == district)]
    fig = px.scatter_mapbox(
        state_df, lat="Latitude", lon="Longitude", color=category,
        color_continuous_scale='Viridis', size=category, size_max=20, zoom=6,
        mapbox_style="carto-positron", width=1200, height=700, hover_name='District',
        hover_data={'State': True, 'Latitude': False, 'Longitude': False}
    )
    fig.update_layout(title=f"Information for {district} in {state} - {category}", title_x=0.34)
    st.plotly_chart(fig, use_container_width=True)


def plot_literacy_rate(category_col, rate_col, category_name, top_bottom, num_states):
    """
    Displays a map of the top or bottom states based on literacy rate.

    Parameters:
    - category_col (str): The literacy category column to analyze.
    - rate_col (str): Column to store the calculated literacy rate.
    - category_name (str): The name of the literacy category (e.g., 'Literacy Rate').
    - top_bottom (str): Whether to show "Top" or "Bottom" states.
    - num_states (int): The number of states to display.
    """
    pop = final_df.groupby('State')['Population'].sum().reset_index()
    literate = final_df.groupby('State')[category_col].sum().reset_index()
    merged_data = pop.merge(literate, on='State')
    merged_data[rate_col] = round((merged_data[category_col] / merged_data['Population']) * 100)
    merged_data = merged_data.merge(state_df, on='State')
    sorted_data = merged_data.sort_values(by=rate_col, ascending=(top_bottom == "Bottom")).head(num_states)
    fig = px.scatter_mapbox(
        sorted_data, lat="Latitude", lon="Longitude", color=rate_col,
        color_continuous_scale='Viridis', size=rate_col, size_max=20, zoom=3,
        mapbox_style="carto-positron", width=1200, height=700, hover_name='State',
        hover_data={'State': True, 'Latitude': False, 'Longitude': False}
    )
    fig.update_layout(title=f"{top_bottom} {num_states} States by {category_name}", title_x=0.34)
    st.plotly_chart(fig, use_container_width=True)


def plot_population(top_bottom, num_states):
    """
    Displays a map of the top or bottom states by population.

    Parameters:
    - top_bottom (str): Whether to show "Top" or "Bottom" states.
    - num_states (int): The number of states to display.
    """
    pop = final_df.groupby('State')['Population'].sum().reset_index()
    merged_data = pop.merge(state_df, on='State')
    sorted_data = merged_data.sort_values(by='Population', ascending=(top_bottom == "Bottom")).head(num_states)
    fig = px.scatter_mapbox(
        sorted_data, lat="Latitude", lon="Longitude", color='Population',
        color_continuous_scale='Viridis', size='Population', size_max=20, zoom=3,
        mapbox_style="carto-positron", width=1200, height=700, hover_name='State',
        hover_data={'State': True, 'Latitude': False, 'Longitude': False}
    )
    fig.update_layout(title=f"{top_bottom} {num_states} States by Population", title_x=0.34)
    st.plotly_chart(fig, use_container_width=True)


def state_category(category, top_bottom, num_states):
    """
    Directs the display of a literacy rate or population map for the top or bottom states.

    Parameters:
    - category (str): The category to analyze (e.g., 'Literacy Rate', 'Population').
    - top_bottom (str): Whether to show "Top" or "Bottom" states.
    - num_states (int): The number of states to display.
    """
    if category == 'Literacy Rate':
        plot_literacy_rate('Literate', 'State_literacy', 'Literacy Rate', top_bottom, num_states)
    elif category == 'Male Literacy Rate':
        plot_literacy_rate('Male_Literate', 'Male_literacy', 'Male Literacy Rate', top_bottom, num_states)
    elif category == 'Female Literacy Rate':
        plot_literacy_rate('Female_Literate', 'Female_literacy', 'Female Literacy Rate', top_bottom, num_states)
    elif category == 'Population':
        plot_population(top_bottom, num_states)


def comparision(district_data, district, category, state):
    """
    Compares a selected district to other districts within the same state in a specified category.

    Parameters:
    - district_data (DataFrame): The data for all districts in the specified state.
    - district (str): The district to highlight in the comparison.
    - category (str): The category to compare across districts.
    - state (str): The state containing the district.
    """
    fig_district = px.scatter(
        district_data, x=category, y=category, color="District",
        labels={category: category}, title=f"{category} Comparison in Districts of {state}",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    selected_district_data = district_data[district_data["District"] == district]
    fig_district.add_scatter(
        x=selected_district_data[category], y=selected_district_data[category],
        mode="markers", marker=dict(color="red", size=15, symbol="circle"),
        name=f"{district} (Selected)"
    )
    st.plotly_chart(fig_district, use_container_width=True)
