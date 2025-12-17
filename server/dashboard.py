import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

st.set_page_config(page_title="NeuroGuard Dashboard", layout="wide")

st.title("🛡️ NeuroGuard - AI Threat Monitor")

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'traffic_data.csv')

def load_data():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    return pd.DataFrame()

# Placeholders for live updates
kpi1, kpi2, kpi3 = st.columns(3)
chart1, chart2 = st.columns(2)

while True:
    df = load_data()
    
    if not df.empty:
        # KPI Metrics
        kpi1.metric("Total Packets", len(df))
        kpi2.metric("Unique IPs", df['Src IP'].nunique())
        
        # Protocol Distribution Chart
        if 'Protocol' in df.columns:
            fig_proto = px.pie(df, names='Protocol', title='Protocol Distribution')
            chart1.plotly_chart(fig_proto, use_container_width=True)
        
        # Top Source IPs Chart
        if 'Src IP' in df.columns:
            top_ips = df['Src IP'].value_counts().head(10)
            fig_ip = px.bar(top_ips, x=top_ips.index, y=top_ips.values, title='Top Active Source IPs')
            chart2.plotly_chart(fig_ip, use_container_width=True)
            
    time.sleep(2)
    st.rerun()