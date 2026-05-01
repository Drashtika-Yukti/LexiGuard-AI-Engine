# --- Stage 1: Build Aegis Studio (Frontend) ---
FROM node:20-slim AS frontend-builder
WORKDIR /app
COPY studio/package*.json ./
RUN npm install
COPY studio/ ./
RUN npm run build

# --- Stage 2: Build Aegis Ingestor (Go) ---
FROM golang:1.21-alpine AS worker-builder
WORKDIR /app
COPY workers/ingestor/ .
RUN go build -o ingestor main.go

# --- Stage 3: Final Production Image ---
FROM python:3.11-slim

# Set up user for Hugging Face Spaces (UID 1000)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"
WORKDIR /home/user/app

# Install build dependencies
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
USER user

# Install Python requirements
COPY --chown=user engine/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy Engine source code
COPY --chown=user engine/ .

# Copy built Frontend (Studio) to engine/static
COPY --from=frontend-builder --chown=user /app/dist ./static

# Copy built Go Ingestor
COPY --from=worker-builder --chown=user /app/ingestor .

# Copy and prepare entrypoint script
COPY --chown=user scripts/entrypoint.sh .
RUN chmod +x entrypoint.sh

# Environment variables for Hugging Face
ENV PORT=7860
EXPOSE 7860

# Start everything
CMD ["./entrypoint.sh"]
