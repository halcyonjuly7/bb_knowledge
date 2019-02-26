FROM python:3.7

COPY ./app/main/project /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["celery",  "-A",  "celery_app.celery_app", "worker", "--loglevel=debug"]