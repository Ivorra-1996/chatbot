FROM python:3.11-slim

# Evita prompts interactivos
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# Paquetes mínimos (agregá build-essential si alguna lib lo pide)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl tini && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt /app/
RUN pip install -r requirements.txt

# Copiamos el resto
COPY app /app

# Streamlit usa 8501 por defecto
EXPOSE 8501

# tini para señalización limpia
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
