# Usamos una versión estable de Python
FROM python:3.10-slim

# Instalamos las herramientas de sistema necesarias (FFmpeg es obligatorio para audio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Definimos el directorio de trabajo
WORKDIR /app

# Primero copiamos el requirements.txt e instalamos las dependencias
# Esto es vital para que 'discord' y 'yt-dlp' se instalen
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Luego copiamos el resto de tu código
COPY . .

# Comando para iniciar el bot
CMD ["python", "main.py"]
