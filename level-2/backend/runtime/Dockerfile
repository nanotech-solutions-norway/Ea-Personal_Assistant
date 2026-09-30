FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/runtime

WORKDIR /app

COPY runtime /app/runtime

EXPOSE 8080

CMD ["python", "-m", "ea_runtime.server"]
