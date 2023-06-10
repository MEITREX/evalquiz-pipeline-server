FROM python:3.10.11-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /evalquiz-pipeline-server
CMD ["gunicorn", "evalquiz-pipeline-server:app", "-b", "0.0.0.0:80"]
