import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="NeuroGuard - Ops Center",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    /* Hide default table indices */
    thead tr th:first-child {display:none}
    tbody th {display:none}
    
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #464b5c;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Settings ---
st.sidebar.title("🛠️ Control Panel")
st.sidebar.markdown("---")

# Refresh Control
auto_refresh = st.sidebar.checkbox("Auto Refresh", value=False) 
refresh_rate = st.sidebar.slider("Rate (sec)", 1, 10, 2)

st.sidebar.markdown("---")
st.sidebar.subheader("🚫 Threat Targeting")

# Target IP Input
blocked_ip_input = st.sidebar.text_input("Suspicious IP (Red):", value="172.20.10.3")
st.sidebar.info(f"'{blocked_ip_input}' -> RED (Blocked)\nOthers -> GREEN (Clean)")

# --- Main Dashboard Layout ---
st.title("🛡️ NeuroGuard - Live Traffic Analysis")

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'traffic_data.csv')

def load_data():
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            if not df.empty and 'Src IP' in df.columns:
                # Classify traffic based on sidebar input
                def classify_threat(ip):
                    if str(ip).strip() == str(blocked_ip_input).strip():
                        return "⛔ ATTACK"
                    return "✅ CLEAN"
                
                df['Status'] = df['Src IP'].apply(classify_threat)
            return df
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- Top Level Metrics ---
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(df)
    # Filter counts based on Status column
    bad_packets = len(df[df['Status'] == "⛔ ATTACK"]) if 'Status' in df.columns else 0
    good_packets = len(df[df['Status'] == "✅ CLEAN"]) if 'Status' in df.columns else 0
    
    col1.metric("Total Packets", total)
    col2.metric("🛡️ Blocked (Threats)", bad_packets, delta_color="inverse")
    col3.metric("✅ Allowed (Clean)", good_packets, delta_color="normal")
    
    top_proto = df['Protocol'].mode()[0] if 'Protocol' in df.columns else "-"
    col4.metric("Protocol", top_proto)

    st.markdown("---")

    # --- Charts Section ---
    c1, c2 = st.columns(2)
    with c1:
        color_map = {"✅ CLEAN": "#2ecc71", "⛔ ATTACK": "#e74c3c"}
        
        if 'Status' in df.columns:
            fig = px.pie(df, names='Status', title='Traffic Health', 
                         color='Status', color_discrete_map=color_map, hole=0.5)
            st.plotly_chart(fig, use_container_width=True)
            
    with c2:
        if 'Src IP' in df.columns:
            # Filter for clean traffic only
            clean_df = df[df['Status'] == "✅ CLEAN"]
            if not clean_df.empty:
                top_clean = clean_df['Src IP'].value_counts().head(5)
                fig2 = px.bar(x=top_clean.index, y=top_clean.values, 
                              title="Top Active CLEAN Hosts", color_discrete_sequence=['#2ecc71'])
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("No clean traffic detected yet. Try opening a browser tab in the background.")

    # --- Live Data Table ---
    st.subheader("📋 Live Stream (Green = Safe / Red = Threat)")
    
    # Show last 100 packets
    latest_df = df.iloc[::-1].head(100)
    
    def color_rows(row):
        if row.get('Status') == "⛔ ATTACK":
            return ['background-color: #581818; color: white'] * len(row)
        else:
            return ['background-color: #1b4d3e; color: white'] * len(row)

    st.dataframe(latest_df.style.apply(color_rows, axis=1), use_container_width=True, height=500)

else:
    st.info("Waiting for data... Please start the Sniffer module.")

# --- Auto Refresh Logic ---
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()