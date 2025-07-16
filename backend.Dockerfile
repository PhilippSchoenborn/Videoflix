FROM python:3.12-alpine

LABEL maintainer="mihai@developerakademie.com"
LABEL version="1.0"
LABEL description="Videoflix Backend - Python 3.12 Alpine"

WORKDIR /app

COPY . .

RUN apk update && \
    apk add --no-cache --upgrade bash curl && \
    apk add --no-cache postgresql-client ffmpeg && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

# Fix line endings and make script executable
RUN sed -i 's/\r$//' backend.entrypoint.sh && \
    chmod +x backend.entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "bash", "./backend.entrypoint.sh" ]
