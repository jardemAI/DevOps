FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --home-dir /app app
COPY --chown=app:app app/ ./app/

USER app
EXPOSE 8000
CMD ["python", "-m", "app.server"]
