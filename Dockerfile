FROM python:3

RUN apt update && apt install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY * .

CMD ["python3", "main.py"]