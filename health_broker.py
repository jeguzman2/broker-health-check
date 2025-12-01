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


def check_service(name, url):
    """Devuelve True si está vivo, False si falló."""
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except:
        return False


def main():
    fails = {name: 0 for name in SERVICES}  # fallas por servicio

    while True:
        for name, url in SERVICES.items():
            healthy = check_service(name, url)

            if healthy:
                print(f" {name} SALUDABLE")
                fails[name] = 0
            else:
                fails[name] += 1
                print(f" {name} FALLA #{fails[name]}")

                if fails[name] >= FAIL_LIMIT:
                    send_email_alert(
                        f"ALERTA: {name} está caído",
                        f"El servicio {name} ha fallado {fails[name]} veces seguidas.\nURL: {url}"
                    )
                    fails[name] = 0

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

