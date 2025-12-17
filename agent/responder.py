from scapy.all import IP, TCP, send

def kill_connection(packet):
    """
    Sends a TCP Reset (RST) packet to terminate the connection.
    """
    # Extract IP and TCP headers
    ip_layer = packet[IP]
    tcp_layer = packet[TCP]

    # Create the RST packet (Spoofing the destination)
    # We pretend to be the 'dst' sending a Reset to 'src'
    rst_pkt = IP(src=ip_layer.dst, dst=ip_layer.src) / \
              TCP(sport=tcp_layer.dport, dport=tcp_layer.sport, 
                  flags="R", seq=tcp_layer.ack, ack=tcp_layer.seq + 1)

    # Send the packet (verbose=0 suppresses default scapy output)
    send(rst_pkt, verbose=0)
    
    print(f">>> [IPS] Kill Packet (RST) Sent! -> {ip_layer.src}")