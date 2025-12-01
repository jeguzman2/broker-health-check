FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY health_broker.py .

# Render necesita que un proceso corra en primer plano.
# Tu script YA corre en un loop infinito, así que funciona perfecto.
CMD ["python", "health_broker.py"]
