FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
RUN mkdir -p projects && useradd -u 10001 -m aegis && chown -R aegis:aegis /app
USER aegis
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
