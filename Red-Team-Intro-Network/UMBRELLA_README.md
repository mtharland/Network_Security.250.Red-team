# Networking & Security Labs

A set of hands-on projects from my intro-to-networking security coursework, focused on understanding core protocol trust assumptions (ARP, DNS, TCP) by building both attacker-side tools and the defenses against them — in isolated lab environments only.

> ⚠️ All projects below were built and tested exclusively on isolated virtual lab networks I own and control. See each repo's README for full disclaimer.

| Project | Focus | Skills |
|---|---|---|
| [ARP MITM Sniffer](link) | Layer 2 spoofing, MITM credential capture | Scapy, raw packet crafting, traffic analysis |
| [DNS Poisoning & Beacon Logger](link) | DNS trust exploitation, C2 detection patterns | DNS protocol, Flask, packet sniffing |
| [Port Scanner & Fingerprinting](link) | Network reconnaissance fundamentals | Socket programming, concurrency, TTL analysis |

Each project pairs an attack simulation with a written explanation of *why* it works and how it's defended against — the goal was to understand network security from both sides, not just run existing tools.

## Dependencies

The ARP MITM and DNS Poisoning projects rely on [Scapy](https://scapy.net/) for raw packet crafting, and the DNS Poisoning project also uses [Flask](https://flask.palletsprojects.com/) for its beacon logging server. The Port Scanner project uses only the Python standard library. Each repo includes its own `requirements.txt` — install with:

```bash
pip install -r requirements.txt
```
