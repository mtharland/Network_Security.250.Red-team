import socket
import argparse

def grab_banner(target, port, timeout=2):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((target, port))
        try:
            banner = s.recv(1024).decode(errors="ignore")
        except socket.timeout:
            banner = ""
        s.close()
        return banner
    except Exception as e:
        return ""

def main():
    parser = argparse.ArgumentParser(description="Banner grabber")
    parser.add_argument("--target", required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    banner = grab_banner(args.target, args.port)
    if banner:
        print(f"[+] Banner from {args.target}:{args.port}")
        print(banner)
    else:
        print("[-] No banner or connection failed.")

if __name__ == "__main__":
    main()
