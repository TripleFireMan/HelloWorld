FROM python:3.7

# 安装netcat
# RUN apt-get update && apt install -y netcat

WORKDIR /app

COPY . /app/

RUN pip3 install --upgrade pip&&pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

# CMD python3 manage.py runserver 0.0.0.0:8000

RUN chmod +x ./start.sh

ENTRYPOINT /bin/bash ./start.sh