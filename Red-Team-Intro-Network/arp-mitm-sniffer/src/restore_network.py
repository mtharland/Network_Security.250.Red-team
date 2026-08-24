from scapy.all import ARP, send
import argparse

def restore(victim_ip, victim_mac, gateway_ip, gateway_mac):
    pkt_victim = ARP(op=2, pdst=victim_ip, psrc=gateway_ip,
                     hwdst=victim_mac, hwsrc=gateway_mac)
    pkt_gateway = ARP(op=2, pdst=gateway_ip, psrc=victim_ip,
                      hwdst=gateway_mac, hwsrc=victim_mac)

    print("[+] Restoring ARP tables...")
    for _ in range(5):
        send(pkt_victim, verbose=False)
        send(pkt_gateway, verbose=False)
    print("[+] Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore ARP tables after spoofing")
    parser.add_argument("--victim-ip", required=True)
    parser.add_argument("--victim-mac", required=True)
    parser.add_argument("--gateway-ip", required=True)
    parser.add_argument("--gateway-mac", required=True)
    args = parser.parse_args()

    restore(args.victim_ip, args.victim_mac, args.gateway_ip, args.gateway_mac)
