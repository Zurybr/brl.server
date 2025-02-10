# Usa una imagen base oficial de Python (en este caso, Python 3.9 slim)
FROM python:3.9-slim

# Evita la generación de archivos .pyc y asegura que la salida se muestre en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias y las instala
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código fuente al contenedor
COPY . .

# Expone el puerto 8000 para la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
