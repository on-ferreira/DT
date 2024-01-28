# Use a base Python image with Alpine Linux
FROM python:3.11.7-alpine3.18 AS builder

# Copy the requirements file into the container at /app
COPY /manager/requirements_manager.txt /DT/requirements.txt

# Install dependencies
RUN python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && apk add --update --no-cache postgresql-dev \
    && /py/bin/pip install -r /DT/requirements.txt


# Stage 2: Create Final Image
FROM python:3.11.7-alpine3.18

LABEL maintainer="DTsistemas"

ENV PYTHONBUFFERED 1

COPY --from=builder /py /py
COPY ./common /DT/common
COPY ./manager /DT/manager

WORKDIR /DT
EXPOSE 5095

ENV PATH="/py/bin:$PATH"

USER root

RUN adduser --disabled-password --no-create-home DTuser \
    && mkdir -p /vol/web/static \
    && mkdir -p /vol/web/media \
    && chown -R DTuser:DTuser /vol \
    && chmod -R 755 /vol

USER DTuser
