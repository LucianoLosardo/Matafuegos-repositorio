# 1. Usamos una imagen de Python ligera (Alpine o Slim son ideales para esto)
FROM python:3.11-slim

# 2. Evitamos que Python genere archivos .pyc y forzamos que los logs salgan directo a la consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /code

# 4. Instalamos dependencias del sistema necesarias para PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiamos el archivo de requerimientos e instalamos las librerías de Python
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiamos todo el contenido de la carpeta backend al contenedor
COPY . /code/

# 7. Comando para ejecutar la app (usando el módulo app.main como hicimos antes
# Agregamos --reload y --host 0.0.0.0 para que sea accesible desde afuera
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]