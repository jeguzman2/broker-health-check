import time
import requests
import smtplib
from email.mime.text import MIMEText

# CONFIGURACIÓN BÁSICA
SERVICES = {
    "SpringBoot Provesi API": "https://micro-pedidos-iua0.onrender.com/actuator/health",
    "FastAPI Inventario": "https://micro-inventario.onrender.com/health",
}
CHECK_INTERVAL = 10  # segundos entre chequeos
FAIL_LIMIT = 5       # fallas consecutivas antes de alerta

# CONFIGURACIÓN DE CORREO (SMTP de Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "santafegod@gmail.com"
FROM_PASSWORD = "dirbjrglphlljnjs"
TO_EMAIL = "juanesteban.guzmanangel@gmail.com"

def send_email_alert(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

def check_health():
    try:
        r = requests.get(HEALTH_URL, timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def main():
    fails = 0
    while True:
        healthy = check_health()
        if healthy:
            print(" Servicio saludable.")
            fails = 0
        else:
            fails += 1
            print(f" Falla detectada #{fails}")
            if fails >= FAIL_LIMIT:
                send_email_alert(
                    "ALERTA: Servicio inactivo",
                    f"El servicio {HEALTH_URL} ha fallado {fails} veces seguidas."
                )
                fails = 0  # reinicia después de alertar
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
