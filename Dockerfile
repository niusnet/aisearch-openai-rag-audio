# Etapa 1: Construir el frontend
FROM node:18 AS frontend-builder

# Establecer el directorio de trabajo para el frontend
WORKDIR /app/frontend

# Copiar el código del frontend
COPY ./app/frontend/ .

# Instalar dependencias y construir el frontend
RUN npm install && npm run build

# Etapa 2: Configurar el backend
FROM python:3.11-slim AS backend

# Establecer el directorio de trabajo para el backend
WORKDIR /app/backend

# Copiar el código del backend
COPY ./app/backend/ .

# Copiar los archivos estáticos construidos del frontend al backend
COPY --from=frontend-builder /app/frontend/dist ./static

# Instalar dependencias del backend
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que se ejecutará el backend
EXPOSE 8000

# Definir el comando por defecto para ejecutar la aplicación backend
CMD ["python", "app.py"]
