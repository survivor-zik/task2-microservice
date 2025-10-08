FROM python:3.12-slim

WORKDIR /app

COPY . /app

ENV OPENAI_API_KEY=${OPENAI_API_KEY:-}

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]