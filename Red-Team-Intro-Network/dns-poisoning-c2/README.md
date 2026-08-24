# DNS Poisoning Simulation & Beacon Logger (Intro Networking — Red Team Lab)

> ⚠️ **Educational Use Only**
> These tools were built for an intro-to-networking security course and tested exclusively in an isolated home-lab environment (local VMs, no internet-facing hosts, no third-party networks). They are not intended for use on any network, system, or device you do not own or do not have explicit written authorization to test. Unauthorized use of ARP spoofing, DNS poisoning, or network scanning tools against networks you don't control may violate computer fraud laws (e.g., the U.S. Computer Fraud and Abuse Act) and similar laws elsewhere.

**Goal:** Show how DNS response spoofing can redirect victims to attacker-controlled infrastructure, and simulate how that infrastructure logs check-ins — to understand DNS trust assumptions and detection strategies like DNS monitoring and DNSSEC.

## Skills demonstrated
- DNS protocol internals (query/response structure, transaction IDs)
- Packet sniffing and on-the-fly forged response injection
- Basic HTTP server development with Flask
- Understanding of C2 (command-and-control) beaconing patterns for detection purposes

## Components
| File | Purpose |
|---|---|
| `dns_spoofer.py` | Listens for DNS queries for a target domain and replies with a forged IP before the real server responds |
| `fake_c2_server.py` (a.k.a. beacon logger) | Simple Flask server simulating attacker infrastructure; logs "beacons" (check-ins) from redirected victims |
| `dns_attack_diagram.md` | Diagram of the spoofing flow (see below) |

## How it works
1. `dns_spoofer.py` sniffs for DNS queries matching a target domain on the lab network.
2. On match, it races a forged DNS response back to the victim pointing at attacker-controlled infrastructure.
3. The victim connects to `fake_c2_server.py`, which logs the IP, User-Agent, and any beacon payload — simulating what a real C2 checks for.

## Lab environment
- Isolated virtual network with no route to the real internet DNS
- Attacker: Linux VM with Python 3, Scapy, Flask
- Victim: separate VM configured to use the attacker as its DNS resolver (lab-only)

## Setup
```bash
pip install -r requirements.txt
sudo python3 dns_spoofer.py --domain example.com --ip <attacker_ip>
python3 fake_c2_server.py
```

## What I learned
- Why DNS spoofing works: no default authentication on UDP/53 responses, and the "first response wins" race condition
- How beaconing/check-in patterns look from the defender's side (useful for building detections)
- Mitigations: DNSSEC, encrypted DNS (DoH/DoT), network-level DNS monitoring, egress filtering