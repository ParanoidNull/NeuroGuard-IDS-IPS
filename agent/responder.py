from scapy.all import IP, TCP, send
import sys

class Renkler:
    KIRMIZI = '\033[91m'
    RESET = '\033[0m'

def baglantiyi_kes(paket):
    """
    Hedef paketi alir ve gonderen kisiye sahte bir RST (Reset) paketi yollar.
    Bu paket 'Baglantiyi derhal kopar' emridir.
    """
    # Sadece TCP paketleri kesilebilir (UDP baglantisizdir)
    if not paket.haslayer(TCP):
        return

    # Paket bilgilerini al
    ip_layer = paket[IP]
    tcp_layer = paket[TCP]

    # --- SALDIRGANA MÜDAHALE ---
    # Sanki hedef biz degilmisiz gibi, hedef adina saldirgana cevap donuyoruz.
    # IP'leri ve Portlari ters ceviriyoruz.
    # Seq numarasi onemli: Saldirganin bekledigi siradaki numara (ACK) olmali.
    
    rst_pkt = IP(src=ip_layer.dst, dst=ip_layer.src) / \
              TCP(sport=tcp_layer.dport, dport=tcp_layer.sport,
                  flags="R", # R = RESET Bayragi
                  seq=tcp_layer.ack, # Onun bekledigi sira
                  ack=0)

    # Sessizce gonder (verbose=0)
    send(rst_pkt, verbose=0)
    
    print(f"{Renkler.KIRMIZI}   >>> [IPS] Baglanti Kesici (RST) Gonderildi! -> {ip_layer.src}{Renkler.RESET}")