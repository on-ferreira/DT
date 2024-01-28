# Use a base Python image with Alpine Linux
FROM python:3.11.7-alpine3.18

LABEL maintainer="DTsistemas"

ENV PYTHONBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./DT/collector/requirements_manager.txt /app/requirements.txt

# Install dependencies
RUN apk add --update --no-cache postgresql-dev \
    && python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r /app/requirements.txt

# Copy the content from DT/common into the container at /app/DT/common
COPY ./DT/common /app/DT/common

# Copy the contents of the collector module into the container at /app/DT/collector
COPY ./DT/manager /app/DT/manager

# Set the working directory to /app/DT/collector
WORKDIR /app/DT/manager

# Create a non-root user for running the application
RUN adduser --disabled-password --no-create-home DTuser && \
    chown -R DTuser:DTuser /app  && \
    chmod -R 755 /app

# Switch to the non-root user
USER DTuser

