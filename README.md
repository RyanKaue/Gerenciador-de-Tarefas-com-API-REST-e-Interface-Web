# Gerenciador de Tarefas com API REST e Interface Web

Um sistema completo de gerenciamento de tarefas com backend em FastAPI, frontend em React, autenticação JWT e sistema de notificações por e-mail.

## Funcionalidades

- Cadastro e login de usuários
- CRUD completo de tarefas
- Sistema de filtros e ordenação
- Autenticação JWT
- Notificações por e-mail 24h antes do prazo das tarefas
- Interface web responsiva

## Tecnologias Utilizadas

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT
- Celery + Redis
- SendGrid

### Frontend
- React
- Material-UI
- React Router
- Axios

## Documentação

- [Documentação da API](./backend/API_DOCUMENTATION.md)
- [Documentação do Código](./CODE_DOCUMENTATION.md)
- [Manual de Instalação e Uso](./INSTALLATION.md)

## Scripts

- `start_services.sh`: Inicia todos os serviços necessários
- `run_tests.sh`: Executa os testes automatizados

## Estrutura do Projeto

```
task-manager/
├── backend/
│   ├── app/
│   │   ├── models/         # Modelos de dados
│   │   ├── schemas/        # Schemas para validação
│   │   ├── routes/         # Rotas da API
│   │   ├── crud/           # Operações de banco de dados
│   │   ├── utils/          # Utilitários
│   │   ├── celery_app.py   # Configuração do Celery
│   │   ├── database.py     # Configuração do banco de dados
│   │   ├── main.py         # Ponto de entrada
│   │   └── tasks.py        # Tarefas do Celery
│   ├── tests/              # Testes automatizados
│   └── API_DOCUMENTATION.md # Documentação da API
├── frontend/
│   ├── public/             # Arquivos estáticos
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── contexts/       # Contextos React
│   │   ├── App.js          # Componente principal
│   │   └── index.js        # Ponto de entrada
│   └── tests/              # Testes automatizados
├── CODE_DOCUMENTATION.md   # Documentação do código
├── INSTALLATION.md         # Manual de instalação e uso
├── start_services.sh       # Script para iniciar serviços
└── run_tests.sh            # Script para executar testes
```

Gerenciador de Tarefas - Manual de Instalação e Uso
Este documento contém instruções detalhadas para instalar, configurar e utilizar o Gerenciador de Tarefas.

Requisitos do Sistema
Python 3.10+
Node.js 16+
PostgreSQL 14+
Redis 6+
Instalação
1. Clonar o Repositório
git clone https://github.com/seu-usuario/gerenciador-tarefas.git
cd gerenciador-tarefas
2. Configurar o Backend
# Criar e ativar ambiente virtual
cd backend
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados PostgreSQL
# Certifique-se de que o PostgreSQL está em execução
sudo service postgresql start
sudo -u postgres psql -c "CREATE USER taskmanager WITH PASSWORD 'taskmanager123';"
sudo -u postgres psql -c "CREATE DATABASE taskmanagerdb OWNER taskmanager;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE taskmanagerdb TO taskmanager;"
3. Configurar o Frontend
# Instalar dependências
cd ../frontend
npm install
4. Configurar o Redis
# Instalar e iniciar o Redis
sudo apt-get install redis-server
sudo service redis-server start
5. Configurar o SendGrid (para notificações por e-mail)
Crie uma conta no SendGrid
Obtenha uma chave de API
Edite o arquivo backend/app/tasks.py e substitua "SUA_CHAVE_API_SENDGRID" pela sua chave de API
Edite o endereço de e-mail remetente (FROM_EMAIL) conforme necessário
Execução
Método 1: Script de Inicialização
O projeto inclui um script que inicia todos os serviços necessários:

# Tornar o script executável
chmod +x start_services.sh

# Executar o script
./start_services.sh
Método 2: Iniciar Serviços Manualmente
Backend (FastAPI)
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Worker do Celery
cd backend
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info
Beat do Celery (para tarefas agendadas)
cd backend
source venv/bin/activate
celery -A app.celery_app beat --loglevel=info
Frontend (React)
cd frontend
npm start
Acesso à Aplicação
Backend (API): http://localhost:8000
Frontend (Interface Web): http://localhost:3000
Documentação da API: http://localhost:8000/docs
Uso da Aplicação
1. Registro e Login
Acesse http://localhost:3000
Clique em "Registrar" para criar uma nova conta
Preencha o formulário com nome, e-mail e senha
Após o registro, faça login com seu e-mail e senha
2. Gerenciamento de Tarefas
Criar Tarefa
Após o login, clique em "Nova Tarefa"
Preencha o formulário com título, descrição, data limite, prioridade e status
Clique em "Criar"
Visualizar Tarefas
Todas as suas tarefas são exibidas na página principal após o login
Use os filtros para encontrar tarefas específicas:
Filtrar por status (pendente, em andamento, concluída)
Filtrar por prioridade (baixa, média, alta)
Filtrar por data limite
Ordenar por diferentes campos
Editar Tarefa
Na lista de tarefas, clique no ícone de edição (lápis) da tarefa desejada
Atualize as informações no formulário
Clique em "Atualizar"
Excluir Tarefa
Na lista de tarefas, clique no ícone de exclusão (lixeira) da tarefa desejada
Confirme a exclusão
3. Sistema de Notificações
O sistema enviará automaticamente e-mails de lembrete 24 horas antes do prazo de cada tarefa. Não é necessária nenhuma configuração adicional pelo usuário.

Execução de Testes
O projeto inclui testes automatizados para o backend e frontend:

# Tornar o script executável
chmod +x run_tests.sh

# Executar os testes
./run_tests.sh
Solução de Problemas
Problemas de Conexão com o Banco de Dados
Verifique se o PostgreSQL está em execução: sudo service postgresql status
Verifique as credenciais no arquivo backend/app/database.py
Problemas com o Redis
Verifique se o Redis está em execução: sudo service redis-server status
Verifique a configuração no arquivo backend/app/celery_app.py
Problemas com o Celery
Verifique os logs: celery_worker.log e celery_beat.log
Certifique-se de que o Redis está funcionando corretamente
Problemas com o Frontend
Verifique se a API está acessível: http://localhost:8000
Verifique os logs: frontend.log
Recursos Adicionais
Documentação da API
Documentação do Código
