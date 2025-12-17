import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Dosya Yolları
LOG_FILE = "logs/traffic_data.csv"
MODEL_FILE = "models/isolation_forest.pkl"
MODEL_DIR = "models"

class Renkler:
    YESIL = '\033[92m'
    MAVI = '\033[94m'
    KIRMIZI = '\033[91m'
    RESET = '\033[0m'

def model_egit():
    print(f"{Renkler.MAVI}--- NeuroGuard AI Egitim Modulu ---{Renkler.RESET}")

    # 1. Veriyi Yukle
    if not os.path.exists(LOG_FILE):
        print(f"{Renkler.KIRMIZI}Hata: Veri dosyasi bulunamadi! Once sniffer.py calistirip veri toplayin.{Renkler.RESET}")
        return

    print("Veri seti yukleniyor...")
    try:
        df = pd.read_csv(LOG_FILE)
    except Exception as e:
        print(f"Hata: CSV okunurken sorun olustu. Dosya bos olabilir. {e}")
        return

    # Veri setinde yeterli veri var mi?
    if len(df) < 50:
        print(f"{Renkler.KIRMIZI}Uyari: Yetersiz veri ({len(df)} satir). Saglikli egitim icin en az 100-200 satir veri toplayin.{Renkler.RESET}")
        return

    # 2. Ozellik Secimi (Feature Selection)
    # AI su an sadece sayisal degerlere bakacak: Kaynak Port, Hedef Port, Paket Boyutu
    # IP adresleri ve Bayraklar (Flags) string oldugu icin MVP asamasinda cikartiyoruz.
    features = ['Src Port', 'Dst Port', 'Length']
    
    # Eksik verileri temizle (varsa)
    X = df[features].dropna()

    print(f"Egitim basladi... ({len(X)} ornek ile)")

    # 3. Modeli Kur (Isolation Forest)
    # contamination=0.01 -> Verinin %1'inin gurultu/anomali olabilecegini varsayiyoruz.
    # random_state=42 -> Her calistirdigimizda ayni sonuclari versin diye sabitliyoruz.
    clf = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    
    clf.fit(X)

    # 4. Modeli Kaydet
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    joblib.dump(clf, MODEL_FILE)
    
    print(f"{Renkler.YESIL}Basarili! Model egitildi ve kaydedildi: {MODEL_FILE}{Renkler.RESET}")
    print("Artik sistem anormallikleri taniyabilir.")

if __name__ == "__main__":
    model_egit()