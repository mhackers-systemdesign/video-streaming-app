FROM python:3.8-slim-buster

WORKDIR flask-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "flask", "--app" , "server", "run", "--host=0.0.0.0"]
