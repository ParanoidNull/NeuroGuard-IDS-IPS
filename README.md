# 🛡️ NeuroGuard - AI Powered IDS/IPS System

> **Autonomous Network Attack Detection and Prevention System with Artificial Intelligence**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![AI](https://img.shields.io/badge/AI-IsolationForest-orange?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-IPS%20%26%20IDS-red?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**NeuroGuard** is a next-generation cybersecurity tool developed to detect modern threats that traditional signature-based firewalls miss. It analyzes network traffic using **Unsupervised Learning**, detects anomalies, and physically terminates the attacker's connection via **TCP Reset (RST) Injection** when a threat is detected.

---

## 🌟 Key Features

### 🧠 1. AI Core (Isolation Forest)
* **Algorithm:** `Isolation Forest` (Scikit-learn).
* **Capability:** Does not rely on pre-defined rules. Learns the "normal" behavior of the network and flags anything deviating from it (including Zero-Day attacks) as an anomaly.

### ⚔️ 2. Hybrid Protection (IDS + IPS)
* **Detection (IDS):** Sniffs traffic using `Scapy` and analyzes packet headers.
* **Prevention (IPS):** Not just alerts. Instantly sends a spoofed **RST (Reset)** packet to the attacker, terminating the connection in milliseconds.

### 📊 3. Live Watchtower (Dashboard)
* Modern web interface based on `Streamlit`.
* Visualizes live traffic flow, protocol distribution, and top active IP addresses in real-time.

### 🚀 4. Cross-Platform & One-Click Setup
* Runs smoothly on **Windows, Linux, and macOS**.
* Automated setup scripts (`.bat` and `.sh`) handle Python environments and dependencies.

---

## 🛠️ Installation & Usage

### 🪟 Windows Users
1.  Right-click on **`baslat.bat`** and select **Run as Administrator**.
2.  The script will automatically set up the environment and launch the menu.
    * *(Note: Install Npcap if prompted).*

### 🐧 Linux & 🍎 macOS Users
1.  Open terminal in the project directory.
2.  Make the script executable (once):
    ```bash
    chmod +x start.sh
    ```
3.  Run it:
    ```bash
    ./start.sh
    ```

---

## ⚠️ Requirements

* **Admin Privileges:** Sniffing network cards requires Root/Admin rights.
* **Npcap (Windows):** Required for Scapy. Install in "API-compatible Mode".

---

## ⚖️ Disclaimer

**NeuroGuard** is developed for educational and research purposes.
* Use this software only on networks you own or have permission to test.
* Unauthorized packet manipulation is illegal. The developer assumes no responsibility for misuse.

---

<p align="center">Made with ❤️ by <b>Cyber Maker</b></p>