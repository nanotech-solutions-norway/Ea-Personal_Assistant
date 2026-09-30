FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/runtime

WORKDIR /app

COPY runtime/requirements-runtime.txt /app/runtime/requirements-runtime.txt
RUN pip install --no-cache-dir -r /app/runtime/requirements-runtime.txt

COPY runtime /app/runtime

EXPOSE 8080

CMD ["python", "-m", "ea_runtime.server"]
