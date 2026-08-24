from flask import Flask, request

app = Flask(__name__)

@app.route("/beacon", methods=["GET", "POST"])
def beacon():
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "")
    data = request.get_data(as_text=True)
    print(f"[+] Beacon from {ip}")
    print(f"    User-Agent: {ua}")
    if data:
        print(f"    Data: {data}")
    return "OK", 200

@app.route("/")
def index():
    return "Fake C2 server. Nothing to see here.", 200

if __name__ == "__main__":
    print("[+] Starting fake C2 server on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)
