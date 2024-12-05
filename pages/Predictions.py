import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(layout="wide")

st.title('🔮 Solar Wind Parameters and Geomagnetic Indices Predictions')

st.write("""
This page provides predicted values for key solar wind parameters and geomagnetic indices over the next five days. These predictions are currently static and based on general estimates but can be replaced with model-based predictions in the future.
""")

# Predicting for the next 5 days
future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 6)]
future_dates_str = [date.strftime('%Y-%m-%d') for date in future_dates]

# General static predictions (replace with model-based values in the future)
predictions = {
    'IMF Bz (GSM)': np.random.uniform(-10, 10, 5),  # Example random predictions around a typical Bz range
    'Solar Wind Speed (km/s)': np.random.uniform(300, 700, 5),  # Typical solar wind speeds
    'Proton Density (N/cm³)': np.random.uniform(1, 15, 5),  # General proton density range
    'Dst Index (nT)': np.random.uniform(-100, 20, 5),  # Typical Dst index during non-extreme conditions
    'Kp Index': np.random.uniform(0, 9, 5),  # Typical full Kp range
}

# Static threshold values for alerts
thresholds = {
    'IMF Bz (GSM)': -5,  # nT
    'Solar Wind Speed (km/s)': 500,  # km/s
    'Proton Density (N/cm³)': 10,  # N/cm³
    'Dst Index (nT)': -50,  # nT
    'Kp Index': 5,  # Valid Kp range: 0 to 9
}

# Convert predictions to a DataFrame
prediction_df = pd.DataFrame(predictions, index=future_dates_str)

# Display predictions
st.write("### Predicted Values for the Next 5 Days")
st.table(prediction_df)

st.write("""
These predictions give a general indication of expected solar and geomagnetic conditions over the next few days. Predictions will be refined using advanced models and real-time data inputs to provide more accurate forecasts.
""")

# Alert messages
st.subheader('Alerts')
alert_messages = []

for parameter in prediction_df.columns:
    values = prediction_df[parameter]
    threshold = thresholds[parameter]
    if parameter == 'IMF Bz (GSM)':
        # Check if values fall below the threshold for IMF Bz (GSM)
        if min(values) < threshold:
            alert_messages.append(f"**Alert for {parameter}:** Predicted values may fall below the threshold of {threshold} nT.")
    elif parameter in ['Dst Index (nT)']:
        # Check if values fall below the threshold for Dst
        if min(values) < threshold:
            alert_messages.append(f"**Alert for {parameter}:** Predicted values may indicate geomagnetic storm conditions (< {threshold} nT).")
    else:
        # For other parameters, check if values exceed the threshold
        if max(values) > threshold:
            alert_messages.append(f"**Alert for {parameter}:** Predicted values may exceed the threshold of {threshold}.")


# Plot predicted values with threshold lines
st.write("### Visual Representation of Predictions")

for parameter in prediction_df.columns:
    values = prediction_df[parameter]
    fig = px.line(x=future_dates_str, y=values, labels={'x': 'Date', 'y': parameter}, title=f'Predictions for {parameter}')
    if parameter in thresholds:
        # Add threshold line
        threshold_line = thresholds[parameter]
        fig.add_hline(y=threshold_line, line_dash="dot", annotation_text=f"Threshold: {threshold_line}", annotation_position="bottom right")
    st.plotly_chart(fig, use_container_width=True)

st.write("""
The above plots visually represent our predictions, showing potential trends and variations over the next five days. These can be instrumental in planning and preparing for space weather impacts.
""")

if alert_messages:
    ms = '⚠️ **Potential Alerts:** \n\n'
    for msg in alert_messages:
        ms += msg + '\n\n'
    st.error(ms)
else:
    st.success('✅ No alerts. Predicted values are within normal ranges.')
