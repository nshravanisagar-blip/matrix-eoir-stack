FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --home-dir /app app

COPY --chown=app:app vision_api/ /app/vision_api/
COPY --chown=app:app inference_worker/ /app/inference_worker/

USER app:app

EXPOSE 8000 9000

CMD ["python", "-u", "vision_api/app.py"]
