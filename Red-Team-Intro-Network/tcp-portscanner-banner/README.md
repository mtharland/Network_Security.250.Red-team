# TCP Port Scanner & Banner Grabber (Intro Networking — Recon Lab)

> ⚠️ **Educational Use Only**
> This tool was built for an intro-to-networking security course and tested exclusively against hosts I own or control on an isolated lab network. Port scanning networks or systems you don't have authorization to test may violate computer fraud laws (e.g., the U.S. Computer Fraud and Abuse Act) and similar laws elsewhere.

**Goal:** Build a basic reconnaissance tool that scans for open TCP ports, grabs service banners, and estimates the target OS — the same first step used in both penetration testing and network inventory/asset management.

## Skills demonstrated
- Socket programming and TCP connect scanning
- Concurrency with `ThreadPoolExecutor` for scan performance
- Service/banner enumeration
- Basic OS fingerprinting via TTL heuristics

## Components
| File | Purpose |
|---|---|
| `scanner.py` | Multithreaded TCP connect scan across a port range |
| `banner_grabber.py` | Connects to an open port and reads the service banner |
| `fingerprint.py` | Uses ICMP TTL values to guess the target OS |
| `protocol_overview.md` | Notes on TCP handshake / ICMP TTL behavior (see below) |

## Setup
```bash
python3 scanner.py --target <ip> --start 1 --end 1024
python3 banner_grabber.py --target <ip> --port <port>
python3 fingerprint.py --target <ip>
```

## What I learned
- How TCP connect scanning differs from SYN/stealth scanning (and why this is the "noisy" version)
- How TTL varies by default OS (Linux ~64, Windows ~128) and why that's an unreliable but useful heuristic
- Basics of banner grabbing for service identification, and why obscuring banners is a defensive practice