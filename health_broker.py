import time
import requests
import smtplib
from email.mime.text import MIMEText

SERVICES = {
    "SpringBoot Provesi API": "https://micro-pedidos-iua0.onrender.com/actuator/health",
    "FastAPI Inventario": "https://micro-inventario.onrender.com/health",
}

CHECK_INTERVAL = 10  
FAIL_LIMIT = 5       

SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
FROM_EMAIL = "provesi.alertas@outlook.com"
FROM_PASSWORD = "pibas123"
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


def is_healthy(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def main():
    fail_count = 0

    while True:
        all_ok = True

        for name, url in SERVICES.items():
            healthy = is_healthy(url)

            if not healthy:
                print(f"❌ {name} FALLÓ → {url}")
                all_ok = False
            else:
                print(f"✅ {name} OK")

        if all_ok:
            fail_count = 0
        else:
            fail_count += 1
            if fail_count >= FAIL_LIMIT:
                send_email_alert(
                    "ALERTA: Uno o más servicios están caídos",
                    f"Health Check detectó {fail_count} fallos consecutivos."
                )
                fail_count = 0

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    print("🚀 Iniciando Broker de Health Checks...")
    main()
