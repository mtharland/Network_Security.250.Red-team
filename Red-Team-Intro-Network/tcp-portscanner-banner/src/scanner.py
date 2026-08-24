import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"[+] Port {port} open")
            return port
    except Exception:
        pass
    finally:
        s.close()
    return None

def scan_range(target, start_port, end_port, workers=100):
    print(f"[+] Scanning {target} from {start_port} to {end_port}")
    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(scan_port, target, p) for p in range(start_port, end_port + 1)]
        for f in futures:
            port = f.result()
            if port:
                open_ports.append(port)
    print(f"[+] Open ports: {open_ports}")
    return open_ports

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("--target", required=True, help="Target IP or hostname")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1024)
    args = parser.parse_args()

    scan_range(args.target, args.start, args.end)
