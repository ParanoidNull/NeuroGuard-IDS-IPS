# 🛡️ NeuroGuard - AI Powered IDS/IPS System

> **Yapay Zeka Destekli, Otonom Ağ Saldırı Tespit ve Engelleme Sistemi**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![AI](https://img.shields.io/badge/AI-IsolationForest-orange?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-IPS%20%26%20IDS-red?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**NeuroGuard**, geleneksel imza tabanlı güvenlik duvarlarının yakalayamadığı modern tehditleri tespit etmek için geliştirilmiş yeni nesil bir siber güvenlik aracıdır. Ağ trafiğini **Gözetimsiz Öğrenme (Unsupervised Learning)** ile analiz eder, anormallikleri saptar ve tehdit algılandığında **TCP Reset (RST) Injection** yöntemiyle saldırganın bağlantısını fiziksel olarak keser.

---

## 🌟 Temel Özellikler

### 🧠 1. Yapay Zeka Beyni (AI Core)
* **Algoritma:** `Isolation Forest` (Scikit-learn).
* **Yetenek:** Önceden tanımlanmış kurallara ihtiyaç duymaz. Ağın "normal" davranışını öğrenir ve bu davranışın dışına çıkan her şeyi (Zero-Day saldırıları dahil) anomali olarak işaretler.

### ⚔️ 2. Hibrit Koruma (IDS + IPS)
* **Tespit (IDS):** Trafiği `Scapy` ile dinler ve paket başlıklarını (IP, Port, Flags, Size) analiz eder.
* **Engelleme (IPS):** Sadece uyarı vermez. Saldırıyı tespit ettiği milisaniye içinde saldırgana sahte bir **RST (Reset)** paketi yollayarak bağlantıyı koparır.

### 📊 3. Canlı Gözetleme Kulesi (Dashboard)
* `Streamlit` tabanlı modern web arayüzü.
* Canlı trafik akışı, protokol dağılımı (pasta grafik) ve en çok konuşan IP adreslerini saniyelik güncellenen grafiklerle sunar.

### 🚀 4. Çapraz Platform ve Otomatik Kurulum
* **Windows, Linux ve macOS** üzerinde sorunsuz çalışır.
* Tek tıkla kurulum scriptleri (`.bat` ve `.sh`) sayesinde Python ortamını (`venv`) ve kütüphaneleri otomatik kurar.

---

## 📂 Proje Mimarisi

Sistem modüler bir yapıya sahiptir:

```text
NeuroGuard-IDS/
├── 📄 main.py           # MERKEZİ YÖNETİM (CLI Menüsü)
├── 📄 baslat.bat        # Windows Otomatik Başlatıcı
├── 📄 baslat.sh         # Linux/macOS Otomatik Başlatıcı
├── 📄 requirements.txt  # Gerekli Kütüphaneler
├── 📂 agent/            # SAHA AJANLARI
│   ├── sniffer.py       # Trafik Dinleyici (Kulak)
│   ├── ids.py           # Karar Mekanizması ve Koruma (Beyin & Kalkan)
│   └── responder.py     # Müdahale Birimi / RST Atıcı (Silah)
├── 📂 server/           # ANALİZ MERKEZİ
│   ├── train_model.py   # AI Eğitim Modülü
│   └── dashboard.py     # Görsel Arayüz
├── 📂 models/           # Eğitilmiş AI Modelleri (.pkl)
└── 📂 logs/             # Trafik Veritabanı (.csv)
---

## 🛠️ Kurulum ve Başlatma (One-Click Setup)

Terminal komutlarıyla uğraşmanıza gerek yok. İşletim sisteminize uygun dosyayı çalıştırın.

### 🪟 Windows Kullanıcıları İçin
1.  Proje klasöründeki **`baslat.bat`** dosyasına **Sağ Tıklayın -> Yönetici Olarak Çalıştır**.
2.  Script otomatik olarak:
    * Python sanal ortamını (venv) kuracak.
    * Gerekli kütüphaneleri yükleyecek.
    * Programı başlatacaktır.
    * *(Not: İlk çalıştırmada Npcap sürücüsü yoksa sizi indirme sayfasına yönlendirir.)*

### 🐧 Linux ve 🍎 macOS Kullanıcıları İçin
1.  Terminali açın ve proje dizinine gelin.
2.  Scripti çalıştırılabilir hale getirin (Tek seferlik):
    ```bash
    chmod +x baslat.sh
    ```
3.  Scripti çalıştırın:
    ```bash
    ./baslat.sh
    ```
4.  Yönetici şifrenizi (sudo) girin ve arkanıza yaslanın.

---

## 🎮 Kullanım Kılavuzu (Menü Seçenekleri)

Program açıldığında sizi merkezi bir CLI menüsü karşılar:

**[1] Veri Toplama Modülü (Sniffer):**
Yapay zekayı eğitmek için ağınızı dinler ve `logs/traffic_data.csv` dosyasına normal trafik verilerini kaydeder.

**[2] Yapay Zeka Eğitimi (Train):**
Toplanan verileri kullanarak AI modelini eğitir ve `models/` klasörüne kaydeder.

**[3] IDS/IPS Koruma Kalkanı (Active Defense):**
Sistemi koruma moduna alır. Trafiği canlı izler, anomali tespit ederse **engeller**.

**[4] Dashboard (Web UI):**
Tarayıcınızda görsel analiz panelini açar. `http://localhost:8501`

**[5] Saldırı Simülasyonu (Test):**
Sistemin tepkisini ölçmek için sahte saldırı paketleri (Port Scan / TCP Flood) oluşturur.

---

## ⚠️ Gereksinimler ve Sorun Giderme

* **Yönetici İzni:** Ağ kartını dinlemek (sniffing) ve paket enjekte etmek (injection) için program **Root/Admin** yetkisiyle çalıştırılmalıdır. Başlatıcı scriptler bunu otomatik ister.
* **Windows için Npcap:** Windows'ta Scapy'nin çalışması için [Npcap](https://npcap.com/) sürücüsünün kurulu olması gerekir. (Kurarken "Install in API-compatible Mode" seçeneğini işaretleyin).
* **macOS İzinleri:** Terminal'e "Full Disk Access" veya ağ izni vermeniz gerekebilir.

---

## ⚖️ Yasal Uyarı (Disclaimer)

**NeuroGuard**, eğitim ve araştırma amaçlı geliştirilmiş bir Siber Güvenlik projesidir.
* Bu yazılımı sadece **sahibi olduğunuz** veya **yazılı izniniz olan** ağlarda kullanın.
* İzinsiz ağlarda saldırı simülasyonu yapmak veya trafiği manipüle etmek suç teşkil edebilir.
* Geliştirici, yazılımın kötüye kullanımından sorumlu tutulamaz.

---

<p align="center">Made with ❤️ by <b>Cyber Maker</b></p>