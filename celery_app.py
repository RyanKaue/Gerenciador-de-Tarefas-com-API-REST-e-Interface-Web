from celery import Celery
from celery.schedules import crontab
import os

# Configuração do Celery
celery_app = Celery(
    'task_manager',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['app.tasks']
)

# Configuração para executar tarefas periódicas
celery_app.conf.beat_schedule = {
    'check-task-deadlines': {
        'task': 'app.tasks.check_task_deadlines',
        'schedule': crontab(hour=8, minute=0),  # Executa todos os dias às 8h
    },
}

celery_app.conf.timezone = 'America/Sao_Paulo'

if __name__ == '__main__':
    celery_app.start()
