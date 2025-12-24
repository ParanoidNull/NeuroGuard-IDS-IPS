# 🛡️ NeuroGuard - AI Powered IDS/IPS System

> **Next-Generation Autonomous Network Defense System**
>
> *Detects anomalies, visualizes threats, and actively terminates malicious connections using Unsupervised Learning.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![AI Core](https://img.shields.io/badge/AI-IsolationForest-orange?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Active%20IPS-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🚀 Overview

**NeuroGuard** is not just a traffic monitor; it's an intelligent defense layer for your network. Traditional firewalls rely on known signatures, failing against Zero-Day attacks. NeuroGuard uses **Isolation Forest** algorithms to learn "normal" network behavior and instantly flag deviations.

When a threat is confirmed, the **IPS Module** injects TCP RST packets to physically sever the attacker's connection before damage can occur.

## ✨ Key Features

### 🧠 1. AI Anomaly Detection
* Uses **Unsupervised Machine Learning** (Scikit-learn) to profile network traffic.
* Detects DoS attacks, Port Scanning, and Data Exfiltration without needing signature updates.

### ⚔️ 2. Active Defense (IPS)
* **Real-time Blocking:** Doesn't just alert; it acts.
* **RST Injection:** Sends forged reset packets to both the attacker and the victim, terminating the session immediately.

### 📊 3. War Room Dashboard
* **Live Visualization:** Interactive web interface powered by `Streamlit` & `Plotly`.
* **Threat Intel:** Color-coded traffic analysis (Green: Clean, Red: Malicious).
* **Dynamic Blacklisting:** Add suspicious IPs to the blocklist on the fly.

### ⚡ 4. Smart Auto-Loader
* No manual setup required. The intelligent `start.bat` script handles Python detection, Virtual Environment creation, and dependency installation automatically.

---

## 🛠️ Installation & Setup

### 🪟 For Windows Users (Recommended)
**Prerequisite:** Install [Npcap](https://npcap.com/) (Select "Install in API-compatible Mode" during setup) for packet capturing.

1.  Clone the repository:
    ```bash
    git clone [https://github.com/ParanoidNull/NeuroGuard-IDS-IPS.git](https://github.com/ParanoidNull/NeuroGuard-IDS-IPS.git)
    cd NeuroGuard-IDS-IPS
    ```
2.  Double-click **`start.bat`**.
    * *The script will automatically set up the Python environment and launch the menu.*

### 🐧 For Linux / macOS Users
1.  Open terminal in the project folder.
2.  Grant execution permissions and run:
    ```bash
    chmod +x start.sh
    sudo ./start.sh
    ```
    * *Note: Root privileges are required for network sniffing.*

---

## 🕹️ Usage Guide

Once the menu launches, follow this workflow:

### **[1] Start Data Collection (Sniffer)**
* **Purpose:** Captures live network traffic to build a dataset.
* **Output:** Saves packet details to `logs/traffic_data.csv`.
* *Tip: Run this first to gather data for the AI to learn.*

### **[2] Train AI Model**
* **Purpose:** Analyzes the captured CSV data.
* **Action:** Trains the `Isolation Forest` model to understand what "normal" traffic looks like.
* **Output:** Saves the trained model to `models/isolation_forest.pkl`.

### **[3] Start AI Protection (IDS/IPS Mode)**
* **Purpose:** The core protection module.
* **Action:** Monitors traffic in real-time using the trained model. If an anomaly is detected, it triggers the **IPS** to block the connection.

### **[4] Launch Dashboard (Web UI)**
* **Purpose:** Opens the "War Room" interface in your browser.
* **Features:**
    * View total traffic and blocked threats.
    * Identify top attackers via charts.
    * Manually flag IPs as "Suspicious" to highlight them in Red.

### **[5] Attack Simulation (Test)**
* **Purpose:** Simulates a SYN Flood attack against a dummy target.
* **Use Case:** Use this to test if NeuroGuard detects and blocks the traffic.

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Scapy is not detected"** | Ensure [Npcap](https://npcap.com/) is installed on Windows. |
| **"Permission Denied"** | Network sniffing requires Admin/Root privileges. Run as Administrator. |
| **"Python not found"** | The `start.bat` script tries to find Python automatically. Ensure Python 3.10+ is installed and added to PATH. |

---

## ⚖️ Legal Disclaimer

**NeuroGuard is strictly for educational and defensive research purposes.**
* Do not use this tool on networks you do not own or have explicit permission to test.
* The developer assumes no liability for any misuse or damage caused by this software.

---
