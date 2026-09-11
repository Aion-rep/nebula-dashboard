FROM python:3.12-slim

# don't create unnecessary bytecode files and don't buffer logs.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .  

RUN useradd --create-home appuser

USER appuser

EXPOSE 5000

CMD ["python","app.py"]
