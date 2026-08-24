import argparse
import subprocess
import platform

def ping_once(target):
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", target]
    else:
        cmd = ["ping", "-c", "1", target]

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode(errors="ignore")
        for line in out.splitlines():
            if "TTL=" in line.upper():
                # Windows ping output: TTL=128
                parts = line.replace("=", " ").split()
                for p in parts:
                    if p.isdigit():
                        return int(p)
    except Exception:
        return None
    return None

def guess_os(ttl):
    if ttl is None:
        return "Unknown"
    if 100 <= ttl <= 130:
        return "Likely Windows"
    if 50 <= ttl <= 70:
        return "Likely Linux/Unix"
    return "Uncertain"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Very simple OS fingerprint via TTL")
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    ttl = ping_once(args.target)
    print(f"[+] Observed TTL: {ttl}")
    print(f"[+] OS guess: {guess_os(ttl)}")
