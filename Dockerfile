FROM ubuntu:24.04
COPY . .
RUN apt update && \
    apt install -y python3-pip && \
    pip install pip -U && \
    pip install -r requirements.txt
