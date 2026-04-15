import network
import socket
import time
import gc
import machine
import binascii

# =========================
# CONFIG
# =========================
SSID = '[Nom_du_reseau]'
PASSWORD = '[Mot_de_passe]'

TARGET = "[IP_Cible]"
SCAN_INTERVAL = 120

boot = time.ticks_ms()
LOGS = []

CACHE = {
    "ports": [],
    "wifi": [],
    "http": ""
}

last_scan = 0

# =========================
# LOG SYSTEM
# =========================
def log(msg):
    t = time.localtime()
    ts = f"{t[3]:02d}:{t[4]:02d}:{t[5]:02d}"
    entry = f"[{ts}] {msg}"

    print(entry)

    LOGS.append(entry)
    if len(LOGS) > 60:
        LOGS.pop(0)

# =========================
# UPTIME
# =========================
def uptime():
    s = time.ticks_diff(time.ticks_ms(), boot) // 1000
    return f"{s//3600}h {(s%3600)//60}m {s%60}s"

# =========================
# WIFI CONNECT
# =========================
def wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    log("▶️Activation WiFi")

    if not wlan.isconnected():
        log("Connexion WiFi...")
        wlan.connect(SSID, PASSWORD)

        while not wlan.isconnected():
            time.sleep(0.2)

    log("✅ WiFi OK → " + wlan.ifconfig()[0])
    return wlan

# =========================
# WIFI SCAN
# =========================
def wifi_scan(wlan):
    log("Scan WiFi...")

    nets = wlan.scan()
    out = []

    for n in nets:
        ssid = n[0].decode() if isinstance(n[0], bytes) else str(n[0])
        bssid = binascii.hexlify(n[1]).decode()
        out.append([ssid, bssid, n[2], n[3], n[4]])

    log(f"WiFi → {len(out)} réseaux")
    return out

# =========================
# PORT SCAN
# =========================
def port_scan(target):
    log("Scan ports...")

    ports = [22, 80, 443, 8080]
    open_ports = []

    for p in ports:
        try:
            gc.collect()

            addr = socket.getaddrinfo(target, p)[0][-1]

            s = socket.socket()
            s.settimeout(0.3)

            s.connect(addr)

            open_ports.append(p)
            log(f"PORT OPEN → {p}")

            s.close()

        except:
            pass

    log(f"Ports trouvés: {len(open_ports)}")
    return open_ports

# =========================
# HTTP INFO
# =========================
def http_info(host):
    log("HTTP scan...")

    ports = [80, 8080]

    for p in ports:
        try:
            gc.collect()

            addr = socket.getaddrinfo(host, p)[0][-1]

            s = socket.socket()
            s.settimeout(1)

            s.connect(addr)

            req = (
                "HEAD / HTTP/1.1\r\n"
                "Host: {}\r\n"
                "Connection: close\r\n\r\n"
            ).format(host)

            s.send(req.encode())

            try:
                data = s.recv(128)
            except:
                data = b"NO DATA"

            s.close()
            del s

            gc.collect()

            log(f"HTTP OK → port {p}")

            return "PORT {} OK | {} bytes".format(p, len(data))

        except Exception as e:
            log(f"HTTP FAIL {p} → {e}")
            try:
                s.close()
            except:
                pass
            gc.collect()

    return "HTTP ERROR (ENOMEM or unreachable)"

# =========================
# CACHE UPDATE (2 MIN ONLY)
# =========================
def maybe_update_cache(wlan):
    global last_scan

    now = time.time()

    if now - last_scan < SCAN_INTERVAL:
        return

    log("🔄 CACHE REFRESH")

    gc.collect()

    CACHE["ports"] = port_scan(TARGET)
    CACHE["wifi"] = wifi_scan(wlan)
    CACHE["http"] = http_info(TARGET)

    last_scan = now

    log("✅ CACHE OK")

# =========================
# HTML PAGE
# =========================
def page(ip, content):
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
body {{
    margin:0;
    font-family: system-ui;
    background:#050b18;
    color:#e5e7eb;
    font-size:16px;
}}

.header {{
    background:#0f172a;
    padding:18px;
    text-align:center;
}}

.title {{
    font-size:24px;
    color:#22c55e;
    font-weight:bold;
}}

.sub {{
    font-size:13px;
    color:#94a3b8;
}}

.container {{
    max-width:1000px;
    margin:auto;
    padding:15px;
}}

button {{
    background:#111827;
    border:1px solid #374151;
    color:white;
    padding:10px 14px;
    margin:5px;
    border-radius:10px;
}}

.card {{
    background:#0f172a;
    border:1px solid #1f2937;
    padding:14px;
    margin:12px 0;
    border-radius:12px;
}}

table {{
    width:100%;
    border-collapse:collapse;
    font-size:14px;
}}

td, th {{
    border:1px solid #1f2937;
    padding:6px;
}}

th {{
    background:#111827;
    color:#60a5fa;
}}
</style>

</head>

<body>

<div class="header">
<div class="title">Pico SOC Dashboard</div>
<div class="sub">IP {ip} | Uptime {uptime()}</div>
</div>

<div style="text-align:center;">
<a href="/?a=wifi"><button>Réseaux</button></a>
<a href="/?a=ports"><button>Ports</button></a>
<a href="/?a=http"><button>HTTP</button></a>
<a href="/?a=sys"><button>Système</button></a>
<a href="/?a=logs"><button>Logs</button></a>
</div>

<div class="container">
{content}
</div>

</body>
</html>
"""

# =========================
# CARDS
# =========================
def card_ports():
    res = CACHE["ports"]

    html = "<div class='card'><h3>Ports</h3>"

    if not res:
        html += "<p style='color:#f87171'>Aucun port ouvert</p>"
    else:
        for p in res:
            html += f"Port {p} OPEN<br>"

    html += "</div>"
    return html


def card_wifi():
    nets = CACHE["wifi"]

    html = "<div class='card'><h3>Réseaux WiFi</h3>"
    html += "<table><tr><th>SSID</th><th>BSSID</th><th>CH</th><th>RSSI</th></tr>"

    for n in nets:
        html += f"<tr><td>{n[0]}</td><td>{n[1]}</td><td>{n[2]}</td><td>{n[3]}</td></tr>"

    html += "</table></div>"
    return html


def card_http():
    return f"<div class='card'><h3>HTTP</h3><pre>{CACHE['http']}</pre></div>"


def card_sys():
    gc.collect()

    info = {
        "CPU MHz": machine.freq() // 1000000,
        "RAM free": gc.mem_free(),
        "RAM used": gc.mem_alloc(),
        "Model": "Pico W"
    }

    html = "<div class='card'><h3>Système</h3><table>"

    for k, v in info.items():
        html += f"<tr><td>{k}</td><td>{v}</td></tr>"

    html += "</table></div>"
    return html


def card_logs():
    html = "<div class='card'><h3>Logs</h3>"

    for l in LOGS[-50:]:
        html += l + "<br>"

    html += "</div>"
    return html

# =========================
# ROUTER
# =========================
def get_action(req):
    try:
        line = req.split(b"\r\n")[0].decode()
        if "a=" in line:
            return line.split("a=")[1].split(" ")[0]
    except:
        pass
    return "wifi"

# =========================
# SERVER
# =========================
def start():
    wlan = wifi()
    ip = wlan.ifconfig()[0]

    addr = socket.getaddrinfo(ip, 80)[0][-1]

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    log("✅ SOC READY")

    while True:
        gc.collect()

        cl, addr = s.accept()
        req = cl.recv(1024)

        action = get_action(req)

        maybe_update_cache(wlan)

        if action == "wifi":
            content = card_wifi()
        elif action == "ports":
            content = card_ports()
        elif action == "http":
            content = card_http()
        elif action == "sys":
            content = card_sys()
        elif action == "logs":
            content = card_logs()
        else:
            content = card_wifi()

        cl.send(page(ip, content))
        cl.close()

# RUN
start()