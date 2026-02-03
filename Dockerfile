# FROM python:3.9-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*

# # Upgrade pip and install requirements
# COPY requirements.txt .
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir --prefer-binary -r requirements.txt && \
#     python -m spacy download en_core_web_sm

# COPY . .

# EXPOSE 8501

# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]


FROM python:3.9-slim

# Prevent python from writing pyc files & enable logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY requirements.txt .

# Upgrade pip & install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

