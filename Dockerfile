FROM python:3.11-buster

WORKDIR /app

RUN pip install poetry==1.8.5
COPY . .
RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "manage.py", "runserver"]
