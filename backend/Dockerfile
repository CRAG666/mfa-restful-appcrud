FROM python:3.8-alpine
WORKDIR /myApi
COPY requirements.txt /myApi/
RUN pip install -r requirements.txt
COPY . /myApi/
ENV FLASK_APP run.py
ENV passmaria db-1234
CMD flask run --host=0.0.0.0
