#!/bin/bash

# Script para executar os testes do Gerenciador de Tarefas

echo "Iniciando testes do Gerenciador de Tarefas..."

# Diretório base do projeto
BASE_DIR="/home/ubuntu/task-manager"

# Verificar se os serviços estão rodando
echo "Verificando se os serviços estão rodando..."
if ! curl -s http://localhost:8000 > /dev/null; then
  echo "O servidor backend não está rodando. Por favor, execute o script start_services.sh primeiro."
  exit 1
fi

if ! curl -s http://localhost:3000 > /dev/null; then
  echo "O servidor frontend não está rodando. Por favor, execute o script start_services.sh primeiro."
  exit 1
fi

# Instalar dependências para testes
echo "Instalando dependências para testes..."
cd $BASE_DIR/backend
source venv/bin/activate
pip install pytest requests selenium webdriver_manager

# Executar testes da API
echo "Executando testes da API..."
cd $BASE_DIR/backend
python -m unittest tests/test_api.py

# Executar testes da UI
echo "Executando testes da UI..."
cd $BASE_DIR/frontend
python ../backend/venv/bin/python tests/test_ui.py

echo "Testes concluídos!"
