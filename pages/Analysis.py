import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
from utils.loader import *

st.set_page_config(layout="wide")

# Load data
with st.spinner('Loading data...'):
    df = load_old_data()

# Preprocess data
df['datetime'] = pd.to_datetime(df['datetime'])
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day

# Remove the fill values for proper handling
fill_values = [9999.9, 99999.9, 9999999, 999.9, 99999, 9999, 99.99, 999.99, 999]
df.replace(fill_values, 0, inplace=True)
df.dropna(inplace=True)

st.title('📊 Historical Analysis of Solar Wind Parameters and Geomagnetic Indices')

st.write("""
This page provides a historical analysis of key solar wind parameters and geomagnetic indices from the OMNI dataset, spanning from 1964 to the present. Through heatmaps and other visualizations, we aim to identify patterns and relationships in the data over time.
""")

# Select parameter to analyze
st.sidebar.title('Parameter Selection')
parameters = {
    'IMF Bz (GSM)': 'bz_gsm',
    'Solar Wind Speed': 'plasma_speed',
    'Proton Density': 'proton_density',
    'Dst Index': 'dst_index',
    'Kp Index': 'kp',
    'AE Index': 'ae_index',
    # Add more parameters if desired
}

parameter_name = st.sidebar.selectbox('Select a parameter to analyze', list(parameters.keys()))
parameter_col = parameters[parameter_name]

# Year selection for heatmap
years = df['year'].unique().tolist()
years.insert(0, 'All')  # Add 'All' option at the beginning
selected_year = st.sidebar.selectbox('Select Year for Heatmap', years)

# Show heatmap according to selected year
if selected_year == 'All':
    # Aggregate data to monthly averages
    monthly_df = df.groupby(['year', 'month'])[parameter_col].mean().reset_index()
    monthly_pivot = monthly_df.pivot(index='year', columns='month', values=parameter_col)

    # Plot heatmap for all years using Plotly
    st.subheader(f'Heatmap of Monthly Average {parameter_name}')

    st.write(f"""
    The heatmap below shows the monthly average values of **{parameter_name}** from 1964 to the present. Each cell represents the average value for a given month and year.
    """)

    fig = px.imshow(monthly_pivot, labels={'x': 'Month', 'y': 'Year', 'color': f'Monthly Average {parameter_name}'},
                    x=monthly_pivot.columns, y=monthly_pivot.index,
                    color_continuous_scale='Viridis', aspect='auto')
    fig.update_layout(title=f'Monthly Average {parameter_name} (1963 - Present)', height=700)
    st.plotly_chart(fig, use_container_width=True)

else:
    # Filter data for the selected year and compute daily averages
    yearly_df = df[df['year'] == selected_year]
    daily_df = yearly_df.groupby(['month', 'day'])[parameter_col].mean().reset_index()
    daily_pivot = daily_df.pivot(index='day', columns='month', values=parameter_col)

    # Plot heatmap for the selected year with daily averages using Plotly
    st.subheader(f'Heatmap of Daily Average {parameter_name} in {selected_year}')

    st.write(f"""
    The heatmap below shows the daily average values of **{parameter_name}** for each month in **{selected_year}**. This detailed view allows you to see intra-month variability.
    """)

    fig = px.imshow(daily_pivot, labels={'x': 'Month', 'y': 'Day', 'color': f'Daily Average {parameter_name}'},
                    x=daily_pivot.columns, y=daily_pivot.index,
                    color_continuous_scale='Viridis', aspect='auto')
    fig.update_layout(title=f'Daily Average {parameter_name} ({selected_year})')
    st.plotly_chart(fig, use_container_width=True)

# Explanatory text
st.write(f"""
The heatmap above provides a visual representation of how **{parameter_name}** has varied over the decades. Darker colors indicate lower values, while brighter colors represent higher values. Trends, seasonal variations, and anomalies can be identified through this visualization.
""")

# Additional Analysis: Time Series Plot of Notable Events
st.subheader(f'Time Series of {parameter_name} During Notable Events')

st.write(f"""
Below you can select a date range to examine the behavior of **{parameter_name}** during specific periods, such as known geomagnetic storms or solar events.
""")

# User inputs for date range
start_date = st.date_input('Start Date', datetime(2000, 1, 1))
end_date = st.date_input('End Date', datetime(2000, 1, 31))

if start_date > end_date:
    st.error('Error: End date must fall after start date.')
else:
    mask = (df['datetime'] >= pd.to_datetime(start_date)) & (df['datetime'] <= pd.to_datetime(end_date))
    df_event = df.loc[mask]

    # Plot the parameter over the selected date range
    fig = px.line(df_event, x='datetime', y=parameter_col, title=f'{parameter_name} from {start_date} to {end_date}')
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"""
    The plot above shows the variation of **{parameter_name}** during the selected period. You can use this tool to explore specific events and observe how the parameter of interest behaved.
    """)

# Correlation Analysis
st.subheader('Correlation Analysis Between Parameters')

st.write("""
Understanding the relationships between different solar wind parameters and geomagnetic indices can provide insights into the mechanisms driving space weather phenomena.
""")

# Select parameters for correlation
param_options = list(parameters.keys())
param1_name = st.selectbox('Select first parameter', param_options, index=0)
param2_name = st.selectbox('Select second parameter', param_options, index=1)

param1_col = parameters[param1_name]
param2_col = parameters[param2_name]

# Scatter plot with regression line
st.write(f'**Scatter Plot of {param1_name} vs {param2_name}**')

# Remove NaN values for both parameters
df_corr = df[[param1_col, param2_col]].dropna()

fig_corr = px.scatter(df_corr, x=param1_col, y=param2_col, trendline='ols',
                      labels={param1_col: param1_name, param2_col: param2_name},
                      title=f'{param1_name} vs {param2_name}')

st.plotly_chart(fig_corr, use_container_width=True)

# Show correlation coefficient
corr_coef = df_corr[param1_col].corr(df_corr[param2_col])
st.write(f'The correlation coefficient between **{param1_name}** and **{param2_name}** is **{corr_coef:.2f}**.')

# Explanatory text
st.write("""
The scatter plot and correlation coefficient indicate the strength and direction of the linear relationship between the selected parameters. A value close to 1 or -1 signifies a strong linear relationship, while a value near 0 indicates a weak or no linear relationship.
""")

# Conclusion
st.subheader('Insights and Observations')

st.write("""
By analyzing the historical data of solar wind parameters and geomagnetic indices, we can observe long-term trends, seasonal patterns, and correlations between different variables. This information is valuable for understanding space weather phenomena and their potential impacts on Earth's environment and technological systems.
""")

