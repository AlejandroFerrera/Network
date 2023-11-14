
FROM python:3.12.0rc2-slim-bullseye
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requeriments.txt
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]