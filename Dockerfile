FROM python:3.13.12-slim

COPY ./requirements.txt /meal-tracker-webapp/requirements.txt

WORKDIR /meal-tracker-webapp

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY ./src /meal-tracker-webapp/

EXPOSE 5002

CMD ["python", "main.py"]