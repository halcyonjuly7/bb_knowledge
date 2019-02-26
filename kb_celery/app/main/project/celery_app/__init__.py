
from celery import Celery

celery_app =  Celery("project", broker="redis://redis@redis//", include=["celery_app.tasks"])

