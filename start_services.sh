#!/bin/bash

# Script para iniciar todos os serviços do Gerenciador de Tarefas

echo "Iniciando serviços do Gerenciador de Tarefas..."

# Diretório base do projeto
BASE_DIR="/home/ubuntu/task-manager"

# Iniciar o Redis (necessário para o Celery)
echo "Iniciando Redis..."
sudo service redis-server start

# Iniciar o PostgreSQL
echo "Iniciando PostgreSQL..."
sudo service postgresql start

# Ativar ambiente virtual do backend
echo "Ativando ambiente virtual..."
cd $BASE_DIR/backend
source venv/bin/activate

# Iniciar o servidor FastAPI
echo "Iniciando servidor FastAPI..."
cd $BASE_DIR/backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
echo "Servidor FastAPI iniciado na porta 8000"

# Iniciar o worker do Celery
echo "Iniciando worker do Celery..."
cd $BASE_DIR/backend
nohup celery -A app.celery_app worker --loglevel=info > celery_worker.log 2>&1 &
echo "Worker do Celery iniciado"

# Iniciar o beat do Celery para tarefas agendadas
echo "Iniciando beat do Celery..."
cd $BASE_DIR/backend
nohup celery -A app.celery_app beat --loglevel=info > celery_beat.log 2>&1 &
echo "Beat do Celery iniciado"

# Iniciar o servidor de desenvolvimento do React
echo "Iniciando servidor de desenvolvimento React..."
cd $BASE_DIR/frontend
nohup npm start > frontend.log 2>&1 &
echo "Servidor React iniciado na porta 3000"

echo "Todos os serviços iniciados com sucesso!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
