FROM python:3.11

RUN apt update && apt install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .

CMD ["python3", "-u", "main.py"]
