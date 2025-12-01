import time
import requests
import smtplib
from email.mime.text import MIMEText

# ============================
# CONFIGURACIÓN DE SERVICIOS
# ============================

SERVICES = {
    "SpringBoot Provesi API":
        "https://micro-pedidos-iua0.onrender.com/actuator/health",

    "FastAPI Inventario":
        "https://micro-inventario.onrender.com/health",
}

CHECK_INTERVAL = 10    # segundos entre chequeos
FAIL_LIMIT = 5         # fallas antes de enviar alerta


# ============================
# CONFIG SMTP
# ============================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "santafegod@gmail.com"
FROM_PASSWORD = "dirbjrglphlljnjs"
TO_EMAIL = "juanesteban.guzmanangel@gmail.com"


# ============================
# ENVÍO DE ALERTAS
# ============================

def send_email_alert(service, fails):
    subject = f"ALERTA: {service} está fallando"
    message = f"El servicio '{service}' ha fallado {fails} veces seguidas."

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

        print(f"📧 ALERTA ENVIADA: {service}")

    except Exception as e:
        print(f"❌ ERROR ENVIANDO CORREO: {e}")


# ============================
# HEALTH CHECK REAL
# ============================

def check_health(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except Exception as e:
        print(f"⚠️ Error al conectar con {url}: {e}")
        return False


# ============================
# LOOP PRINCIPAL
# ============================

def main():
    print("🚀 Iniciando Health Broker...")
    print("⏳ Esperando 20 segundos para que Render habilite red...")
    time.sleep(20)

    fails = {name: 0 for name in SERVICES}

    while True:
        print("\n====================")
        print("🔍 Chequeando servicios...")
        print("====================")

        for name, url in SERVICES.items():
            healthy = check_health(url)

            if healthy:
                print(f"🟢 {name} OK")
                fails[name] = 0

            else:
                fails[name] += 1
                print(f"🔴 {name} FALLÓ #{fails[name]}")

                if fails[name] >= FAIL_LIMIT:
                    send_email_alert(name, fails[name])
                    fails[name] = 0  # reset después de alertar

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
