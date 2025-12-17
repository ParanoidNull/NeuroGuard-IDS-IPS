from scapy.all import IP, TCP, send, RandShort
import time

# HEDEFI DEGISTIRDIK: Trafik ag kartindan ciksin diye disari (Google) atiyoruz.
hedef_ip = "8.8.8.8" 
hedef_port = 666   # Bu port IDS.py icinde "Yasakli" olarak tanimli

print(f"Saldiri baslatiliyor... Hedef: {hedef_ip}:{hedef_port} (TCP)")

for i in range(5):
    try:
        # TCP Syn paketi
        pkt = IP(dst=hedef_ip) / TCP(dport=hedef_port, flags="S", sport=RandShort())
        send(pkt, verbose=0)
        print(f"[{i+1}] Saldiri paketi yollandi! -> {hedef_ip}")
        time.sleep(1)
    except Exception as e:
        print(f"Hata: {e}")

print("Saldiri bitti.")
time.sleep(2)