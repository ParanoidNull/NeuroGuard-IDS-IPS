import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os
import sys

# Define Paths
# We navigate up from 'server/' to root, then to 'logs/' and 'models/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'traffic_data.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_FILE = os.path.join(MODEL_DIR, 'isolation_forest.pkl')

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    RESET = '\033[0m'

def train():
    print(f"{Colors.BLUE}--- NeuroGuard AI Training Module ---{Colors.RESET}")

    # 1. Load Data
    if not os.path.exists(LOG_FILE):
        print(f"{Colors.RED}[ERROR] Data file not found! Please run 'Sniffer' first to collect data.{Colors.RESET}")
        return

    print("Loading dataset...")
    try:
        df = pd.read_csv(LOG_FILE)
    except Exception as e:
        print(f"Error reading CSV. File might be empty. Details: {e}")
        return

    # Check Data Quality
    if len(df) < 50:
        print(f"{Colors.RED}[WARNING] Insufficient data ({len(df)} rows). Capture at least 100-200 packets for better results.{Colors.RESET}")
        return

    # 2. Feature Selection
    # AI looks at numerical values: Source Port, Destination Port, Packet Length
    features = ['Src Port', 'Dst Port', 'Length']
    
    # Check if required columns exist
    if not all(col in df.columns for col in features):
        print(f"{Colors.RED}[ERROR] CSV is missing required columns: {features}{Colors.RESET}")
        return

    # Drop missing values
    X = df[features].dropna()

    print(f"Training started with {len(X)} samples...")

    # 3. Build Model (Isolation Forest)
    # contamination=0.01 -> We assume ~1% of data might be anomalies/noise
    # random_state=42 -> Fixed seed for reproducibility
    clf = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    
    clf.fit(X)

    # 4. Save Model
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    joblib.dump(clf, MODEL_FILE)
    
    print(f"{Colors.GREEN}[SUCCESS] Model trained and saved to: {MODEL_FILE}{Colors.RESET}")
    print("System is now ready to detect anomalies.")

if __name__ == "__main__":
    train()