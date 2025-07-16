FROM python:3.13-slim
 
RUN mkdir /app
 
WORKDIR /app
 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
RUN apt-get update -y && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /app/entrypoint.sh
 
COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]