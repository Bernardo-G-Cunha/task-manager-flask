FROM python:3.12-slim

WORKDIR /app

# evita arquivos pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# dependências sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# copiar dependências
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copiar código
COPY . .

# porta
EXPOSE 8000

# comando padrão

CMD flask db upgrade && gunicorn run:app --bind 0.0.0.0:8000