FROM python:3.12.11-slim

LABEL org.opencontainers.image.title="edu/attendance-service" \
      org.opencontainers.image.version="0.5.0"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8006 \
    MESSAGE="Attendance online" \
    APP_VERSION=0.5.0 \
    DATA_DIR=/data

WORKDIR /app

RUN groupadd --gid 10006 appuser \
 && useradd --uid 10006 --gid 10006 --no-create-home --shell /usr/sbin/nologin appuser \
 && mkdir /data \
 && chown appuser:appuser /data

COPY --chown=appuser:appuser pract3.py .

USER appuser

EXPOSE 8006

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["python", "-c", "import os, urllib.request as u; u.urlopen('http://127.0.0.1:%s/health' % os.environ['PORT'], timeout=2)"]

CMD ["python", "pract3.py"]


