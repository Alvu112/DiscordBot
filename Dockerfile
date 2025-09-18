# Version python
FROM python:3.11-slim

# Evita caches innecesarios de pip y buffers
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONUNBUFFERED=1

# Directorio
WORKDIR /app

# Copia todo el repositorio
COPY . /app

# Instala librerías de Python
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /app/restart.sh

# Ejecutar Bot
CMD ["sh", "/app/restart.sh"]
