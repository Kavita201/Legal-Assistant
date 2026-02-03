# -------- Builder stage --------
FROM python:3.9 AS builder

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm

# -------- Runtime stage --------
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py","--server.port=8501","--server.address=0.0.0.0","--server.headless=true"]
