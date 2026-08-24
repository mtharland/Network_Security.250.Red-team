# ARP MITM Sniffer (Intro Networking — Red Team Lab)

> ⚠️ **Educational Use Only**
> These tools were built for an intro-to-networking security course and tested exclusively in an isolated home-lab environment (local VMs, no internet-facing hosts, no third-party networks). They are not intended for use on any network, system, or device you do not own or do not have explicit written authorization to test. Unauthorized use of ARP spoofing, DNS poisoning, or network scanning tools against networks you don't control may violate computer fraud laws (e.g., the U.S. Computer Fraud and Abuse Act) and similar laws elsewhere.

**Goal:** Demonstrate ARP spoofing and man-in-the-middle credential capture on a local network to understand how unauthenticated Layer 2 protocols can be abused, and why defenses like dynamic ARP inspection and encrypted transport (HTTPS) matter.

## Skills demonstrated
- Raw packet crafting with Scapy (ARP, IP, TCP layers)
- Man-in-the-middle attack mechanics at Layer 2
- Live traffic capture and HTTP parsing
- Network cleanup / attack reversal

## Components
| File | Purpose |
|---|---|
| `arp_spoofer.py` | Sends forged ARP replies to victim and gateway to redirect traffic through the attacker machine |
| `packet_sniffer.py` | Captures HTTP POST requests and extracts plaintext credentials |
| `restore_network.py` | Restores correct ARP mappings when the attack stops |
| `mitm_flow.md` | Diagram/walkthrough of the attack flow (see below) |

## How it works
1. `arp_spoofer.py` poisons the ARP caches of the victim and gateway so both believe the attacker's MAC address owns the other's IP.
2. Traffic between victim and gateway now flows through the attacker machine (with IP forwarding enabled).
3. `packet_sniffer.py` inspects that traffic for HTTP credentials.
4. `restore_network.py` sends correct ARP replies to repair both hosts' caches when finished.

## Lab environment
- Isolated virtual network (VirtualBox/VMware host-only or NAT network)
- Attacker: Linux VM with Python 3 + Scapy
- Victim: separate VM on the same virtual subnet
- Gateway: virtual router or a third VM acting as gateway

## Setup
```bash
pip install -r requirements.txt
sudo python3 arp_spoofer.py --victim <victim_ip> --gateway <gateway_ip> --mac <attacker_mac>
sudo python3 packet_sniffer.py
# when done:
sudo python3 restore_network.py --victim-ip <ip> --victim-mac <mac> --gateway-ip <ip> --gateway-mac <mac>
```

## What I learned
- Why ARP has no built-in authentication and how that's exploited
- How MITM position enables traffic interception even on switched networks
- Why HTTPS + certificate validation defeats plaintext credential sniffing
- Practical mitigations: static ARP entries, DAI (Dynamic ARP Inspection), 802.1X