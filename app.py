import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import GraphFunctions as gf

st.set_page_config(layout='wide')

# Load the census data
df = pd.read_csv('India.csv')
df["State_District"] = df["State"] + " --- " + df["District"]
st.sidebar.title("India Census 2011 Data Analysis")
analysis_option = st.sidebar.selectbox("Select Analysis Type", [
    "Overall Data Analysis",
    "Districts of the state",
    "Number of Districts by State",
    "Category-wise State Comparison",
    "District-Level Analysis",
    "List Information"
])

# Improve Overall Data Analysis: Add descriptive statistics
if analysis_option == "Overall Data Analysis":
    st.header("Overall Data Analysis 🔍")

    states = df["State"].unique().tolist()
    states.insert(0, 'Overall India')
    state = st.selectbox("Select State", states)

    Primary_level = st.selectbox("Select Primary Level", list(df.columns[5:df.shape[1] - 1]))
    Secondary_level = st.selectbox("Select Secondary Level", list(df.columns[5:df.shape[1] - 1]))

    gf.overall(state, Primary_level, Secondary_level)

    # Descriptive statistics for the selected state
    if state != "Overall India":
        st.subheader("📊 Descriptive Statistics for " + state)
        state_data = df[df["State"] == state]
        st.write(state_data.describe().transpose().iloc[:,1:])

# Top Districts: Add rankings and heatmap visualization
elif analysis_option == "Districts of the state":
    st.header("Districts of the state ")

    # State and category selection in the main interface
    state = st.selectbox("Select State", df["State"].unique())
    category = st.selectbox("Select Category", list(df.columns[5:df.shape[1] - 1]))
    top_bottom = st.selectbox(f"Select Top or Bottom District of {state}", ["Top", "Bottom"])
    num_districts = st.slider("Number of Districts", 1, 10, 5)  # Slider for number of states

    # Filter data for the selected state
    state_data = df[df['State'] == state]
    total_districts = state_data['District'].nunique()
    if num_districts > total_districts:
        # Display message if not enough districts are available
        st.warning(f"There are only {total_districts} districts in {state}. Showing available districts.")
        num_districts = total_districts  # Adjust to the maximum available

    # Dynamic header reflecting user's selection
    st.header(f"{top_bottom} {num_districts} Districts in {state} by {category} 📊")

    # Pass the filtered districts to the function for visualization
    gf.district_category(state, category,top_bottom, num_districts)

# Number of Districts by State: Improved bar chart and map
elif analysis_option == "Number of Districts by State":
    st.header("Number of Districts by State 🗺️")

    state = st.selectbox("Select State", df["State"].unique())

    # Show number of districts in the selected state
    gf.plot_state_on_map(state)
    total_district = len(df[df['State'] == state]['District'].unique())

    # Display the total number of districts in the selected state
    # st.header(f"District Information for {state}")
    st.write(f"**Total Number of Districts in {state}:** {total_district}")

    # Show a table of districts in the selected state
    st.subheader("Districts List")
    st.dataframe(df[df['State'] == state][['District']].drop_duplicates().reset_index(drop=True))
    # Add a bar chart showing number of districts in each state
    # district_counts = df[df['State'] == state]['District'].value_counts().reset_index()
    # district_counts.columns = ["State", "Number of Districts"]
    # fig_districts = px.bar(district_counts, x="State", y="Number of Districts",
    #                        title="Number of Districts by State", color="State")
    # st.plotly_chart(fig_districts)

# Category-wise State Comparison: Use a choropleth map for comparison
elif analysis_option == "Category-wise State Comparison":
    st.header("Category-wise State Comparison 📊")

    category = st.selectbox("Select Category",
                            ['Literacy Rate', 'Male Literacy Rate', 'Female Literacy Rate', 'Population'])
    top_bottom = st.selectbox("Select Top or Bottom States", ["Top", "Bottom"])

    num_states = st.slider("Number of States", 1, 10, 5)  # Display a slider to select 1 to 10 states, default to 5

    # Call the function with selected options
    gf.state_category(category, top_bottom, num_states)



# District-Level Analysis: Include more detailed metrics
elif analysis_option == "District-Level Analysis":
    st.header("District-Level Analysis 📍")

    # Select state, district, and category
    state = st.selectbox("Select State", df["State"].unique())
    district = st.selectbox("Select District", df[df["State"] == state]["District"].unique())
    category = st.selectbox("Select Category", list(df.columns[5:df.shape[1] - 1]))

    # Display selected district information
    gf.state_District_information(state, district, category)

    # Prepare data for scatter plot
    st.subheader(f"📉 Comparison of {district} to All Districts in {state} - {category}")
    district_data = df[df["State"] == state]
    gf.comparision(district_data,district,category,state)



# List Information: Enhanced with better visualizations and analysis
elif analysis_option == "List Information":
    st.header("📊 List Information")

    # Basic Demographic Information by State
    st.subheader("🌍 State Demographics Overview")
    state_demographics = df.groupby("State")[
        ["Population", "literacy_rate", "Male", "Female", "sex_ratio"]].mean().reset_index()
    st.dataframe(state_demographics)

    # Add descriptive statistics summary
    st.subheader("📝 Summary Statistics for Demographic Data")
    st.write(df[["Population", "literacy_rate", "Male", "Female", "sex_ratio"]].describe())

    # Top and Bottom States by Key Metrics
    st.subheader("🏆 Top and Bottom States by Literacy Rate")
    top_lit = df.groupby("State")["literacy_rate"].mean().nlargest(5)
    bottom_lit = df.groupby("State")["literacy_rate"].mean().nsmallest(5)
    st.write("Top 5 States by Literacy Rate:", top_lit)
    st.write("Bottom 5 States by Literacy Rate:", bottom_lit)

    # State with Highest and Lowest Population
    st.subheader("🌟 State with Highest and Lowest Population")
    highest_population = df.groupby("State")["Population"].sum().idxmax()
    lowest_population = df.groupby("State")["Population"].sum().idxmin()
    st.write(f"State with Highest Population: {highest_population} 🏙️")
    st.write(f"State with Lowest Population: {lowest_population} 🌄")

    # Population Distribution by Gender (Pie chart)
    st.subheader("👨‍👩‍👧‍👦 Population Distribution by Gender")
    gender_population = df.groupby("State")[["Male", "Female"]].sum().reset_index()
    fig_gender_population = px.pie(gender_population, names="State", values="Male",
                                   title="Gender Population Distribution")
    st.plotly_chart(fig_gender_population)

    # Literacy Rate Comparison by Gender (Bar chart)
    st.subheader("📚 Literacy Rate Comparison by Gender")
    gender_literacy_rate = df.groupby("State")[["Male_literacy_rate", "Female_literacy_rate"]].mean().reset_index()
    fig_gender_literacy = px.bar(gender_literacy_rate, x="State", y=["Male_literacy_rate", "Female_literacy_rate"],
                                 title="Literacy Rate Comparison by Gender", barmode="group")
    st.plotly_chart(fig_gender_literacy)

    # Household Data Summary (Bar chart)
    st.subheader("🏠 Household Infrastructure")
    household_data = df[["Housholds_with_Electric_Lighting", "Households_with_Internet",
                         "Households_with_Computer"]].mean().reset_index()
    fig_household_data = px.bar(household_data, x="index", y=0,
                                labels={"index": "Household Category", "0": "Percentage"},
                                title="Household Infrastructure")
    st.plotly_chart(fig_household_data)

    # District-Level Statistics
    st.subheader("📍 District-Level Statistics")
    state_district_counts = df["State"].value_counts().reset_index(name="District Count")
    st.write("Number of Districts per State:", state_district_counts)

    # Top 5 districts by Literacy Rate
    st.subheader("🏅 Top 5 Districts by Literacy Rate")
    top_districts = df[["District", "literacy_rate", "Population"]].sort_values(by="literacy_rate",
                                                                                ascending=False).head(5)
    st.write("Top 5 Districts by Literacy Rate:", top_districts)

    # Districts with Highest and Lowest Literacy Rate
    st.subheader("📉 Districts with Highest and Lowest Literacy Rate")
    highest_lit_district = df[["District", "literacy_rate"]].nlargest(1, "literacy_rate")
    lowest_lit_district = df[["District", "literacy_rate"]].nsmallest(1, "literacy_rate")
    st.write("District with Highest Literacy Rate: ", highest_lit_district)
    st.write("District with Lowest Literacy Rate: ", lowest_lit_district)

    # Sex Ratio Distribution (Histogram)
    st.subheader("⚖️ Sex Ratio Distribution")
    fig_sex_ratio = px.histogram(df, x="sex_ratio", nbins=20, title="Sex Ratio Distribution")
    st.plotly_chart(fig_sex_ratio)

    # Population vs Literacy Rate (Scatter plot)
    st.subheader("💡 Population vs Literacy Rate")
    fig_population_literacy = px.scatter(df, x="Population", y="literacy_rate", title="Population vs Literacy Rate")
    st.plotly_chart(fig_population_literacy)

    # Sex Ratio vs Literacy Rate (Scatter plot)
    st.subheader("💑 Sex Ratio vs Literacy Rate")
    scatter_data = df[["sex_ratio", "literacy_rate"]].dropna()
    fig_scatter = px.scatter(scatter_data, x="sex_ratio", y="literacy_rate", title="Sex Ratio vs Literacy Rate")
    st.plotly_chart(fig_scatter)

    # Literacy Levels Distribution (Bar chart)
    st.subheader("📖 Literacy Levels Distribution")
    literacy_counts = df[["Literate", "Male_Literate", "Female_Literate"]].sum().reset_index(name="Count")
    fig_literacy_levels = px.bar(literacy_counts, x="index", y="Count",
                                 labels={"index": "Literacy Level", "Count": "Count"},
                                 title="Literacy Levels Distribution")
    st.plotly_chart(fig_literacy_levels)

    # Downloadable Summary Report
    st.subheader("📥 Downloadable Summary Report")
    csv = df.to_csv(index=False)
    st.download_button(label="Download Census Summary as CSV", data=csv, mime="text/csv")

footer = """
    <style>
        .footer {
            position: relative;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px;
            text-align: center;
            font-size: 12px;
            margin-top: 30px;
            color: #ffffff;
        }
    </style>
    <div class="footer">
        <p>"Statistics are sourced from the 2011 Indian Census." 📅</p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)

