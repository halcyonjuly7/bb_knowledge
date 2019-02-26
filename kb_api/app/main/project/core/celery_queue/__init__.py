from celery import Celery

celery_app = Celery("celery_queue", broker="redis://redis@redis//", incude=["project.tasks"])