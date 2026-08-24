# ARP MITM Attack Flow

## Before the attack — normal traffic

```mermaid
sequenceDiagram
    participant V as Victim
    participant G as Gateway/Router

    V->>G: HTTP request (direct)
    G->>V: HTTP response (direct)
```

Victim and gateway talk directly. Each has the other's *correct* MAC address cached in its ARP table.

## Step 1 — ARP poisoning

```mermaid
sequenceDiagram
    participant V as Victim
    participant A as Attacker
    participant G as Gateway/Router

    A->>V: Forged ARP reply: "Gateway IP is at Attacker MAC"
    A->>G: Forged ARP reply: "Victim IP is at Attacker MAC"
    Note over V,G: Both ARP caches now poisoned
```

`arp_spoofer.py` sends unsolicited ARP replies to both sides. Neither victim nor gateway verifies who actually sent the reply — ARP has no authentication — so both caches get overwritten with the attacker's MAC.

## Step 2 — Traffic flows through the attacker

```mermaid
flowchart LR
    V[Victim] -->|thinks this is Gateway| A[Attacker MAC]
    A -->|forwards traffic| G[Gateway]
    G -->|response| A
    A -->|thinks this is Victim| V

    A -.->|sniffs & logs| S[packet_sniffer.py]
```

With IP forwarding enabled on the attacker machine, traffic is invisibly relayed so the connection still works — but every packet passes through the attacker first, where `packet_sniffer.py` inspects HTTP traffic for credentials.

## Step 3 — Cleanup

```mermaid
sequenceDiagram
    participant V as Victim
    participant A as Attacker
    participant G as Gateway/Router

    A->>V: Correct ARP reply: "Gateway IP is at Gateway MAC"
    A->>G: Correct ARP reply: "Victim IP is at Victim MAC"
    Note over V,G: ARP caches restored, MITM position lost
```

`restore_network.py` sends the *true* ARP mappings so both hosts revert to talking directly, closing the MITM window.

## Why this works

ARP is a stateless, unauthenticated broadcast protocol — any host on the local segment can claim to own any IP address, and other hosts will believe the most recent reply. There's no signature, no challenge/response, nothing to verify.

## Real-world defenses

- **Dynamic ARP Inspection (DAI)** on managed switches — validates ARP packets against a trusted DHCP snooping table
- **Static ARP entries** for critical hosts (gateway, servers)
- **802.1X port authentication** to control who can even join the segment
- **Encrypted transport (HTTPS/TLS)** — doesn't stop the MITM position, but stops the attacker from reading the actual content
