# Gerenciador de Tarefas - Manual de Instalação e Uso

Este documento contém instruções detalhadas para instalar, configurar e utilizar o Gerenciador de Tarefas.

## Requisitos do Sistema

- Python 3.10+
- Node.js 16+
- PostgreSQL 14+
- Redis 6+

## Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/gerenciador-tarefas.git
cd gerenciador-tarefas
```

### 2. Configurar o Backend

```bash
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
```

### 3. Configurar o Frontend

```bash
# Instalar dependências
cd ../frontend
npm install
```

### 4. Configurar o Redis

```bash
# Instalar e iniciar o Redis
sudo apt-get install redis-server
sudo service redis-server start
```

### 5. Configurar o SendGrid (para notificações por e-mail)

1. Crie uma conta no [SendGrid](https://sendgrid.com/)
2. Obtenha uma chave de API
3. Edite o arquivo `backend/app/tasks.py` e substitua `"SUA_CHAVE_API_SENDGRID"` pela sua chave de API
4. Edite o endereço de e-mail remetente (`FROM_EMAIL`) conforme necessário

## Execução

### Método 1: Script de Inicialização

O projeto inclui um script que inicia todos os serviços necessários:

```bash
# Tornar o script executável
chmod +x start_services.sh

# Executar o script
./start_services.sh
```

### Método 2: Iniciar Serviços Manualmente

#### Backend (FastAPI)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Worker do Celery

```bash
cd backend
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

#### Beat do Celery (para tarefas agendadas)

```bash
cd backend
source venv/bin/activate
celery -A app.celery_app beat --loglevel=info
```

#### Frontend (React)

```bash
cd frontend
npm start
```

## Acesso à Aplicação

- **Backend (API)**: http://localhost:8000
- **Frontend (Interface Web)**: http://localhost:3000
- **Documentação da API**: http://localhost:8000/docs

## Uso da Aplicação

### 1. Registro e Login

1. Acesse http://localhost:3000
2. Clique em "Registrar" para criar uma nova conta
3. Preencha o formulário com nome, e-mail e senha
4. Após o registro, faça login com seu e-mail e senha

### 2. Gerenciamento de Tarefas

#### Criar Tarefa

1. Após o login, clique em "Nova Tarefa"
2. Preencha o formulário com título, descrição, data limite, prioridade e status
3. Clique em "Criar"

#### Visualizar Tarefas

- Todas as suas tarefas são exibidas na página principal após o login
- Use os filtros para encontrar tarefas específicas:
  - Filtrar por status (pendente, em andamento, concluída)
  - Filtrar por prioridade (baixa, média, alta)
  - Filtrar por data limite
  - Ordenar por diferentes campos

#### Editar Tarefa

1. Na lista de tarefas, clique no ícone de edição (lápis) da tarefa desejada
2. Atualize as informações no formulário
3. Clique em "Atualizar"

#### Excluir Tarefa

1. Na lista de tarefas, clique no ícone de exclusão (lixeira) da tarefa desejada
2. Confirme a exclusão

### 3. Sistema de Notificações

O sistema enviará automaticamente e-mails de lembrete 24 horas antes do prazo de cada tarefa. Não é necessária nenhuma configuração adicional pelo usuário.

## Execução de Testes

O projeto inclui testes automatizados para o backend e frontend:

```bash
# Tornar o script executável
chmod +x run_tests.sh

# Executar os testes
./run_tests.sh
```

## Solução de Problemas

### Problemas de Conexão com o Banco de Dados

- Verifique se o PostgreSQL está em execução: `sudo service postgresql status`
- Verifique as credenciais no arquivo `backend/app/database.py`

### Problemas com o Redis

- Verifique se o Redis está em execução: `sudo service redis-server status`
- Verifique a configuração no arquivo `backend/app/celery_app.py`

### Problemas com o Celery

- Verifique os logs: `celery_worker.log` e `celery_beat.log`
- Certifique-se de que o Redis está funcionando corretamente

### Problemas com o Frontend

- Verifique se a API está acessível: http://localhost:8000
- Verifique os logs: `frontend.log`

## Recursos Adicionais

- [Documentação da API](./backend/API_DOCUMENTATION.md)
- [Documentação do Código](./CODE_DOCUMENTATION.md)
