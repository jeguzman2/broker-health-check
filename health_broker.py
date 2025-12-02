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

# CONFIGURACIÓN SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "juanesteban.guzmanangel@gmail.com"
FROM_PASSWORD = "qgmvdowajqchxtzz"
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

def check_services():
    """Revisa cada servicio y retorna una lista de los caídos."""
    failed = []

    for name, url in SERVICES.items():
        try:
            r = requests.get(url, timeout=5)
            if r.status_code != 200:
                failed.append(name)
        except Exception:
            failed.append(name)

    return failed

def main():
    fail_count = 0

    while True:
        failed_services = check_services()

        if len(failed_services) == 0:
            print("Todos los servicios están saludables ✔️")
            fail_count = 0

        else:
            fail_count += 1
            print(f"⚠️ Servicios fallando: {failed_services} (fallo #{fail_count})")

            if fail_count >= FAIL_LIMIT:
                failed_list_text = "\n".join(f"- {s}" for s in failed_services)

                send_email_alert(
                    "ALERTA: Servicios caídos",
                    f"Los siguientes servicios fallaron {fail_count} veces consecutivas:\n\n{failed_list_text}"
                )

                fail_count = 0  # Reinicia después de enviar el correo

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
