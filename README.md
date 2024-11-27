

# India Census 2011 Data Analysis

This project provides an interactive web application for analyzing India's 2011 Census data. Built using Streamlit, Pandas, and Plotly, the app enables users to explore state and district-level information on various demographics, such as education levels, across the country.

https://india-census-dashboard-favrwbfqfjtynsglgp7xpb.streamlit.app/ 

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Data Files](#data-files)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)



## Features

- **Interactive Dashboard**: Choose from different types of analyses using a user-friendly sidebar.
- **State and District Analysis**: Explore census data at both state and district levels.
- **Map Visualizations**: Analyze educational metrics using interactive maps with color and size encodings.
- **Custom Comparisons**: Compare data across different states based on user-selected education levels or demographics.

## Demo

A live demo of the app can be run locally (see [Usage](#usage) below). The app enables users to:

1. Select a state or view data for all of India.
2. Choose educational metrics (e.g., primary and secondary education levels) for comparison.
3. Visualize the data on interactive maps and graphs.

## Installation

### Prerequisites

To set up the project, ensure that you have the following installed:

- Python 3.7 or above
- Pip package manager

### Setup Instructions

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/india-census-analysis.git
    cd india-census-analysis
    ```

2. **Install dependencies**:

    Install the required Python libraries by running:

    ```bash
    pip install streamlit pandas plotly
    ```

3. **Download the data files**:

   Ensure the following CSV files are placed in the project directory:
   
   - `India.csv` (2011 Census data for India)
   - `Latitude and Longitude State wise centroids 2020.csv` (state-wise geographical centroids for map plotting)

## Data Files

- **India.csv**: Contains detailed census data, including state, district, and various demographic information.
- **Latitude and Longitude State wise centroids 2020.csv**: Provides the geographical centroids of states for mapping purposes.

Both files are essential for running the analysis and generating visualizations.

## Usage

### Running the App

To start the Streamlit app, run the following command in your terminal:

```bash
streamlit run app.py
```
4. **Sidebar Controls**
   Once the app is running, use the sidebar to choose from several types of analyses:
   
- **Overall Data Analysis:** View aggregated data for all states and districts.
- **Districts of a State:** Drill down into specific states to explore district-level data.
- **Number of Districts by State:** Compare the number of districts across different states.
- **Category-wise State Comparison:** Compare states based on educational or demographic levels.
- **District-Level Analysis:** Visualize and compare district-level metrics.

5. **Visualizations**
- `Bubble Map:` Display educational comparisons (e.g., primary vs. secondary education levels) on a map, where bubble size and color represent the metrics.
- `State and District-Level Graphs:` Visualize census data for specific states and districts using interactive bar charts and scatter plots.

6. **File Descriptions**
- `app.py:` The main script for the Streamlit application. It defines the layout, loads the data, and creates the interactive dashboard with options to analyze and visualize the census data.
- `GraphFunctions.py:` Contains the functions for creating various visualizations (e.g., maps and charts). This includes plotting functions for comparing educational levels and other metrics across states and districts.

7. **Screenshots**



https://github.com/user-attachments/assets/2ae38f42-4168-4d08-b7ee-7ffe50153ad3



   
