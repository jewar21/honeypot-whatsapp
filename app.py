from flask import Flask, request, render_template_string
from datetime import datetime
import logging

app = Flask(__name__)

# Configura el logger
logging.basicConfig(filename='honeypot_log.txt', level=logging.INFO)

# Página señuelo
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Verificación de cuenta</title>
</head>
<body>
    <h2>Estamos verificando tu acceso</h2>
    <p>Por favor espera un momento...</p>
</body>
</html>
"""

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] IP: {ip}, Navegador: {user_agent}"
    print(log_entry)
    logging.info(log_entry)

    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
