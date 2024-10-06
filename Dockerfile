# Stage 1: Build the frontend
FROM node:18 AS frontend-builder

# Set the working directory for the frontend
WORKDIR /app/frontend

# Copy the frontend code
COPY ./app/frontend/ .

# Install dependencies and build the frontend
RUN npm install && npm run build

# Stage 2: Set up the backend
FROM python:3.11-slim AS backend

# Set the working directory for the backend
WORKDIR /app/backend

# Copy the backend code
COPY ./app/backend/ .

# Copy the built static files from the frontend to the backend
COPY --from=frontend-builder /app/frontend/dist ./static

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the backend will run
EXPOSE 8000

# Define the default command to run the backend application
CMD ["python", "app.py"]
