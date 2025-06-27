from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

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

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] IP: {ip}, User-Agent: {user_agent}"
    print(log_entry)  # Esto aparece en la consola de Replit

    # También podrías guardar en archivo si lo prefieres:
    with open("honeypot_log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

    return render_template_string(HTML)

app.run(host='0.0.0.0', port=81)
