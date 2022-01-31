FROM python:3.9.1-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG ROOT_APP=/app/

RUN mkdir $ROOT_APP

WORKDIR $ROOT_APP

RUN apt-get update && apt-get install -y netcat

COPY app/Pipfile app/Pipfile.lock $ROOT_APP

RUN pip install --upgrade pip
RUN python -m pip install --upgrade pipenv wheel
RUN pipenv install --system --ignore-pipfile

COPY app/src $ROOT_APP

COPY docker/wait-services.sh $ROOT_APP
RUN chmod +x wait-services.sh

CMD ["./wait-services.sh", "gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
