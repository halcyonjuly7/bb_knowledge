FROM python:3.7
COPY ./app/main/project /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn",  "-b","0.0.0.0:5555", "--worker-class", "sanic.worker.GunicornWorker", "run:app_factory()"]