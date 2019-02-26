FROM python:3.7
COPY ./app/main/project /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:7777", "run:app_factory()"]