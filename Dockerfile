# Use Python 3.11.3 on Alpine Linux as the base image
FROM python:3.11.3-alpine

# Set maintainer information
LABEL maintainer="aleksanderkedziora"

# Set environment variable to ensure Python operates in buffered mode
ENV PYTHONBUFFERED 1

# Copy requirements file to a temporary directory
COPY ./backend/requirements.txt /tmp/backend/requirements.txt

# Copy application code to /backend directory
COPY ./backend /backend

# Set the working directory to /backend
WORKDIR /backend

# Install dependencies and clean up
RUN apk add --update --no-cache python3 && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base musl-dev zlib zlib-dev linux-headers && \
    pip install --upgrade pip && \
    pip install -r /tmp/backend/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
      --disabled-password \
      --no-create-home \
      django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

# Switch to the django-user for running subsequent commands
USER django-user
