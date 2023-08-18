FROM python:3.10.11-slim-buster

WORKDIR /evalquiz-pipeline-server
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# https://techoverflow.net/2021/01/13/how-to-use-apt-install-correctly-in-your-dockerfile/
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y pandoc && rm -rf /var/lib/apt/lists/*