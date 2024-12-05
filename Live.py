import pandas as pd
import streamlit as st 
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.loader import *

st.set_page_config(layout="wide", page_icon='random')

# Assuming df is already loaded and contains the data

with st.spinner('Loading data...'):
    df = load_data()

# Replace fill values with NaN for proper handling

st.title('🪨 Solar Wind Parameters and Geomagnetic Indices Report')

# Time range selection
st.sidebar.title('Select Time Range')
time_range = st.sidebar.selectbox('Time Range', ['Last Few Hours', 'Last 1 Day', 'Last Week'])

now = datetime.now()
now = datetime.now() - timedelta(days=30)  # Remove this line or comment it out
# st.write(now)  # Optional: Display current time

if time_range == 'Last Few Hours':
    start_time = now - timedelta(hours=6)
elif time_range == 'Last 1 Day':
    start_time = now - timedelta(days=1)
elif time_range == 'Last Week':
    start_time = now - timedelta(weeks=1)

df_time_filtered = df[(df['datetime'] >= start_time) & (df['datetime'] <= now)]

st.write(f"**Showing data from {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {now.strftime('%Y-%m-%d %H:%M:%S')}**")

# Define thresholds
bz_threshold = -5  # nT
speed_threshold = 500  # km/s
density_threshold = 10  # N/cm³
dst_threshold = -50  # nT

# Plotting IMF Bz (GSM)
st.subheader('Interplanetary Magnetic Field Bz (GSM)')

fig_bz = go.Figure()
fig_bz.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=df_time_filtered['bz_gsm'], mode='lines', name='Bz GSM', line=dict(color='blue')))
fig_bz.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=[bz_threshold]*len(df_time_filtered), mode='lines', name='Threshold', line=dict(color='red', dash='dash')))
fig_bz.update_layout(title='IMF Bz (GSM)', xaxis_title='Time', yaxis_title='Bz (nT)', template='plotly_dark')
st.plotly_chart(fig_bz, use_container_width=True)
st.write("The **IMF Bz** (Interplanetary Magnetic Field Bz component) is crucial for space weather. When it's southward, especially below **-5 nT**, it can connect with the Earth's magnetic field, potentially leading to geomagnetic storms.")

# Plotting Solar Wind Speed
st.subheader('Solar Wind Speed')

fig_speed = go.Figure()
fig_speed.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=df_time_filtered['plasma_speed'], mode='lines', name='Solar Wind Speed', line=dict(color='green')))
fig_speed.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=[speed_threshold]*len(df_time_filtered), mode='lines', name='Threshold', line=dict(color='red', dash='dash')))
fig_speed.update_layout(title='Solar Wind Speed', xaxis_title='Time', yaxis_title='Speed (km/s)', template='plotly_dark')
st.plotly_chart(fig_speed, use_container_width=True)
st.write("**Solar Wind Speed** above **500 km/s** can enhance the interaction with Earth's magnetosphere, potentially leading to increased geomagnetic activity.")

# Plotting Proton Density
st.subheader('Proton Density')

fig_density = go.Figure()
fig_density.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=df_time_filtered['proton_density'], mode='lines', name='Proton Density', line=dict(color='orange')))
fig_density.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=[density_threshold]*len(df_time_filtered), mode='lines', name='Threshold', line=dict(color='red', dash='dash')))
fig_density.update_layout(title='Proton Density', xaxis_title='Time', yaxis_title='Density (N/cm³)', template='plotly_dark')
st.plotly_chart(fig_density, use_container_width=True)
st.write("High **Proton Density** over **10 N/cm³** can intensify space weather effects, impacting satellite operations and communications.")

# Geomagnetic Indices
st.subheader('Geomagnetic Indices')

col1, col2 = st.columns(2)

with col1:
    st.write('**Dst Index**')
    fig_dst = go.Figure()
    fig_dst.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=df_time_filtered['dst_index'], mode='lines', name='Dst Index', line=dict(color='purple')))
    fig_dst.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=[dst_threshold]*len(df_time_filtered), mode='lines', name='Threshold', line=dict(color='red', dash='dash')))
    fig_dst.update_layout(title='Dst Index', xaxis_title='Time', yaxis_title='Dst (nT)', template='plotly_dark')
    st.plotly_chart(fig_dst, use_container_width=True)
    st.write("The **Dst Index** measures global geomagnetic storm activity. Values below **-50 nT** indicate storm-level disturbances, affecting navigation systems and power grids.")

with col2:
    st.write('**Kp Index**')
    fig_kp = go.Figure()
    fig_kp.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=df_time_filtered['kp'], mode='lines+markers', name='Kp Index', line=dict(color='cyan')))
    fig_kp.update_layout(title='Kp Index', xaxis_title='Time', yaxis_title='Kp', template='plotly_dark')
    st.plotly_chart(fig_kp, use_container_width=True)
    st.write("The **Kp Index** quantifies geomagnetic activity. Higher values indicate more intense geomagnetic storms, which can affect power systems and satellite operations.")

# Electric Field and Flow Pressure
st.subheader('Electric Field and Flow Pressure')

col3, col4 = st.columns(2)

with col3:
    st.write('**Electric Field**')
    fig_efield = go.Figure()
    fig_efield.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=df_time_filtered['electric_field'], mode='lines', name='Electric Field', line=dict(color='magenta')))
    fig_efield.update_layout(title='Electric Field', xaxis_title='Time', yaxis_title='E (mV/m)', template='plotly_dark')
    st.plotly_chart(fig_efield, use_container_width=True)
    st.write("The **Electric Field** affects charged particles in the solar wind. Large electric field magnitudes can enhance geomagnetic activity and radio signal disruptions.")

with col4:
    st.write('**Flow Pressure**')
    fig_pressure = go.Figure()
    fig_pressure.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=df_time_filtered['flow_pressure'], mode='lines', name='Flow Pressure', line=dict(color='yellow')))
    fig_pressure.update_layout(title='Flow Pressure', xaxis_title='Time', yaxis_title='Pressure (nPa)', template='plotly_dark')
    st.plotly_chart(fig_pressure, use_container_width=True)
    st.write("**Flow Pressure** is influenced by solar wind density and speed. High flow pressure can compress Earth's magnetosphere, impacting space weather conditions.")

# AE Index
st.subheader('AE Index')

fig_ae = go.Figure()
fig_ae.add_trace(go.Scatter(x=df_time_filtered['datetime'], y=df_time_filtered['ae_index'], mode='lines', name='AE Index', line=dict(color='lightgreen')))
fig_ae.update_layout(title='AE Index', xaxis_title='Time', yaxis_title='AE (nT)', template='plotly_dark')
st.plotly_chart(fig_ae, use_container_width=True)
st.write("The **AE Index** measures auroral electrojet activity, reflecting ionospheric currents. High AE values can indicate increased ionospheric disturbances.")

# Summary and Alerts
st.subheader('Summary')

alert_messages = []

def get_threshold_periods(df, column, threshold, condition='less'):
    if condition == 'less':
        condition_met = df[column] < threshold
    elif condition == 'greater':
        condition_met = df[column] > threshold
    else:
        raise ValueError("Condition must be 'less' or 'greater'")
    periods = []
    start_time = None
    for i in range(len(condition_met)):
        if condition_met.iloc[i]:
            if start_time is None:
                start_time = df['datetime'].iloc[i]
            end_time = df['datetime'].iloc[i]
        else:
            if start_time is not None:
                periods.append((start_time, end_time))
                start_time = None
    if start_time is not None:
        periods.append((start_time, end_time))
    return periods

# IMF Bz
bz_periods = get_threshold_periods(df_time_filtered, 'bz_gsm', bz_threshold, condition='less')
if bz_periods:
    alert_messages.append(f"**IMF Bz** was southward and below threshold ({bz_threshold} nT) during the following periods:")
    for period in bz_periods:
        start_str = period[0].strftime('%Y-%m-%d %H:%M')
        end_str = period[1].strftime('%Y-%m-%d %H:%M')
        alert_messages.append(f"- From {start_str} to {end_str}")

# Solar Wind Speed
speed_periods = get_threshold_periods(df_time_filtered, 'plasma_speed', speed_threshold, condition='greater')
if speed_periods:
    alert_messages.append(f"**Solar Wind Speed** was high and above threshold ({speed_threshold} km/s) during the following periods:")
    for period in speed_periods:
        start_str = period[0].strftime('%Y-%m-%d %H:%M')
        end_str = period[1].strftime('%Y-%m-%d %H:%M')
        alert_messages.append(f"- From {start_str} to {end_str}")

# Proton Density
density_periods = get_threshold_periods(df_time_filtered, 'proton_density', density_threshold, condition='greater')
if density_periods:
    alert_messages.append(f"**Proton Density** was high and above threshold ({density_threshold} N/cm³) during the following periods:")
    for period in density_periods:
        start_str = period[0].strftime('%Y-%m-%d %H:%M')
        end_str = period[1].strftime('%Y-%m-%d %H:%M')
        alert_messages.append(f"- From {start_str} to {end_str}")

# Dst Index
dst_periods = get_threshold_periods(df_time_filtered, 'dst_index', dst_threshold, condition='less')
if dst_periods:
    alert_messages.append(f"**Dst Index** indicated geomagnetic storm conditions (below {dst_threshold} nT) during the following periods:")
    for period in dst_periods:
        start_str = period[0].strftime('%Y-%m-%d %H:%M')
        end_str = period[1].strftime('%Y-%m-%d %H:%M')
        alert_messages.append(f"- From {start_str} to {end_str}")

if alert_messages:
    ms = '⚠️ **Alerts:** \n\n'
    for msg in alert_messages:
        ms += msg + '\n\n'
    st.error(ms)
else:
    st.success('✅ No alerts. Solar parameters are within normal ranges.')