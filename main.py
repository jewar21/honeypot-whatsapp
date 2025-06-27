from flask import Flask, request, render_template_string
from datetime import datetime
import requests

app = Flask(__name__)

# Configura tu bot aquí
TELEGRAM_TOKEN = '8055178101:AAGWM1JVaAuZmaJIYL9dQnpoycE3Qh9y8pk'
TELEGRAM_CHAT_ID = '759863630'

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Verificación</title>
</head>
<body>
    <h2>Estamos verificando tu acceso</h2>
    <p>Espera un momento mientras validamos tu identidad...</p>
</body>
</html>
"""

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error enviando a Telegram:", e)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        location = f"{geo.get('country')}, {geo.get('regionName')}, {geo.get('city')}"
    except:
        location = "Ubicación desconocida"

    log_entry = (
        f"🕵️ Nuevo acceso al honeypot:\n"
        f"📆 {timestamp}\n"
        f"🌐 IP: {ip}\n"
        f"📍 Ubicación: {location}\n"
        f"🧠 User-Agent: {user_agent}"
    )

    print(log_entry)

    with open("honeypot_log.txt", "a") as log_file:
        log_file.write(log_entry + "\\n")

    send_telegram_message(log_entry)

    return render_template_string(HTML)

# Ejecutar el servidor en Replit
app.run(host='0.0.0.0', port=81)