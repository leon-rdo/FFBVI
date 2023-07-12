from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo Django como padrão para a configuração do Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '.settings')

# Crie uma instância do aplicativo Celery
app = Celery('ffbvi')

# Configure as opções do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregue as tarefas do aplicativo
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
