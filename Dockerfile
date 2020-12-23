FROM ubuntu:20.04

LABEL name="httpbinasync"
LABEL version="0.1.0"
LABEL description="A simple HTTP service."

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt update -y && apt install python3-pip git -y 
ADD . /opt/httpbinasync

EXPOSE 80

CMD ["python3","main.py"]