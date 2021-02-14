FROM python:3.7
# RUN apk add git
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY VoyagerTutorial.ipynb ./