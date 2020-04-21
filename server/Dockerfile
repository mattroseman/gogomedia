FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

# RUN COMMAND
CMD ["python", "app.py"]
