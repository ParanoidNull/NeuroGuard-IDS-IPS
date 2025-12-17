import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

# Sayfa Ayarlari
st.set_page_config(
    page_title="NeuroGuard Dashboard",
    page_icon="🛡️",
    layout="wide",
)

# Baslik
st.title("🛡️ NeuroGuard - AI Destekli Siber Guvenlik Merkezi")
st.markdown("---")

# Log Dosyasi Yolu
LOG_FILE = "logs/traffic_data.csv"

def veriyi_yukle():
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame() # Bos don
    
    # CSV'yi oku
    try:
        df = pd.read_csv(LOG_FILE)
        # Sona eklenenler en yeni oldugu icin ters cevir (En ustte en yeniler)
        return df.iloc[::-1] 
    except:
        return pd.DataFrame()

# Otomatik Yenileme icin Placeholder
placeholder = st.empty()

# --- CANLI AKIS DONGUSU ---
try:
    while True:
        df = veriyi_yukle()
        
        with placeholder.container():
            if df.empty:
                st.warning("Henuz veri yok. Lutfen 'agent/sniffer.py' veya 'ids.py' calistirin.")
            else:
                # --- UST BILGI KARTLARI (METRICS) ---
                kpi1, kpi2, kpi3 = st.columns(3)
                
                toplam_paket = len(df)
                benzersiz_ip = df['Src IP'].nunique()
                son_islem = df.iloc[0]['Timestamp'] if not df.empty else "-"
                
                kpi1.metric(label="Toplam Yakalanan Paket", value=toplam_paket)
                kpi2.metric(label="Benzersiz Saldirgan/Kaynak", value=benzersiz_ip)
                kpi3.metric(label="Son Islem Zamani", value=son_islem)

                st.markdown("---")

                # --- GRAFIKLER ---
                col1, col2 = st.columns(2)
                
                # Her dongude benzersiz bir key olusturmak icin zaman damgasi (timestamp) kullaniyoruz
                zaman_damgasi = time.time()

                with col1:
                    st.subheader("📡 Protokol Dagilimi")
                    if "Protocol" in df.columns:
                        fig_proto = px.pie(df, names='Protocol', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                        
                        # DUZELTME: key artik dinamik (her saniye degisiyor)
                        st.plotly_chart(fig_proto, use_container_width=True, key=f"grafik_protokol_{zaman_damgasi}")

                with col2:
                    st.subheader("📊 En Cok Konusan IP'ler")
                    if "Src IP" in df.columns:
                        top_ips = df['Src IP'].value_counts().head(10).reset_index()
                        top_ips.columns = ['IP Adresi', 'Paket Sayisi']
                        fig_bar = px.bar(top_ips, x='Paket Sayisi', y='IP Adresi', orientation='h', color='Paket Sayisi')
                        
                        # DUZELTME: key artik dinamik
                        st.plotly_chart(fig_bar, use_container_width=True, key=f"grafik_ip_{zaman_damgasi}")

                # --- DETAYLI TABLO ---
                st.subheader("📋 Canli Trafik Loglari")
                st.dataframe(df, use_container_width=True)

        # 2 saniyede bir sayfayi yenile
        time.sleep(2)

except KeyboardInterrupt:
    print("Dashboard kapatildi.")