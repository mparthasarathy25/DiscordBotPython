FROM python:3.8-slim-buster

WORKDIR /app

COPY req1.txt req1.txt
RUN pip3 install -r req1.txt

COPY . .


RUN apt-get update && apt-get install -y ffmpeg

CMD ["python3", "main.py"]