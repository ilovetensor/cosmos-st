
import streamlit as st
import pandas as pd


@st.cache_data
def load_data():

    filen = "latest.dat"
    cols = ['year', 'day', 'hour', 'bartels_rotation', 'id_imf_spacecraft', 'id_sw_plasma_spacecraft', 'n_imf_avg', 'n_plasma_avg', 'field_magnitude_avg', 'magnitude_avg_field_vector', 'lat_angle_avg_field_vector', 'long_angle_avg_field_vector', 'bx_gse', 'by_gse', 'bz_gse', 'by_gsm', 'bz_gsm', 'sigma_field_magnitude', 'sigma_field_vector', 'sigma_bx', 'sigma_by', 'sigma_bz', 'proton_temperature', 'proton_density', 'plasma_speed', 'plasma_flow_long_angle', 'plasma_flow_lat_angle', 'na_np', 'flow_pressure', 'sigma_t', 'sigma_n', 'sigma_v', 'sigma_phi_v', 'sigma_theta_v', 'sigma_na_np', 'electric_field', 'plasma_beta', 'alfven_mach_number', 'kp', 'r', 'dst_index', 'ae_index', 'proton_flux_1', 'proton_flux_2', 'proton_flux_4', 'proton_flux_10', 'proton_flux_30', 'proton_flux_60', 'flag', 'ap_index', 'f10.7_index', 'pc_n_index', 'al_index', 'au_index', 'magnetosonic_mach_number']

    df = pd.read_csv(filen, sep=r'\s+', header=None, names=cols)
    # df = pd.read_csv('last.csv')
    df['datetime'] = pd.to_datetime(df['year'].astype(str) + ' ' + df['day'].astype(str) + ' ' + df['hour'].astype(str), format='%Y %j %H')
    df.dropna(inplace=True)
    return df

@st.cache_data
def load_old_data():
    filen = "here.dat"
    cols = ['year', 'day', 'hour', 'bartels_rotation', 'id_imf_spacecraft', 'id_sw_plasma_spacecraft', 'n_imf_avg', 'n_plasma_avg', 'field_magnitude_avg', 'magnitude_avg_field_vector', 'lat_angle_avg_field_vector', 'long_angle_avg_field_vector', 'bx_gse', 'by_gse', 'bz_gse', 'by_gsm', 'bz_gsm', 'sigma_field_magnitude', 'sigma_field_vector', 'sigma_bx', 'sigma_by', 'sigma_bz', 'proton_temperature', 'proton_density', 'plasma_speed', 'plasma_flow_long_angle', 'plasma_flow_lat_angle', 'na_np', 'flow_pressure', 'sigma_t', 'sigma_n', 'sigma_v', 'sigma_phi_v', 'sigma_theta_v', 'sigma_na_np', 'electric_field', 'plasma_beta', 'alfven_mach_number', 'kp', 'r', 'dst_index', 'ae_index', 'proton_flux_1', 'proton_flux_2', 'proton_flux_4', 'proton_flux_10', 'proton_flux_30', 'proton_flux_60', 'flag', 'ap_index', 'f10.7_index', 'pc_n_index', 'al_index', 'au_index', 'magnetosonic_mach_number']

    df = pd.read_csv(filen, sep=r'\s+', header=None, names=cols)
    # df = pd.read_csv('last.csv')
    df['datetime'] = pd.to_datetime(df['year'].astype(str) + ' ' + df['day'].astype(str) + ' ' + df['hour'].astype(str), format='%Y %j %H')
    df.dropna(inplace=True)
    return df
