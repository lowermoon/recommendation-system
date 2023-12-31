FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y  sudo libsm6 libxext6 libxrender-dev libglib2.0-0 libgl1-mesa-glx

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV DISPLAY =:99
RUN pip3 install --upgrade pip &&\
    pip3 install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app