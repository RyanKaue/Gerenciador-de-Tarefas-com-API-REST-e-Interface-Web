# Documentação do Código - Gerenciador de Tarefas

## Estrutura do Projeto

O projeto está organizado em duas partes principais:

### Backend (FastAPI)

```
backend/
├── app/
│   ├── models/         # Modelos de dados SQLAlchemy
│   ├── schemas/        # Schemas Pydantic para validação
│   ├── routes/         # Rotas da API
│   ├── crud/           # Operações de banco de dados
│   ├── utils/          # Utilitários (autenticação, etc.)
│   ├── celery_app.py   # Configuração do Celery
│   ├── database.py     # Configuração do banco de dados
│   ├── main.py         # Ponto de entrada da aplicação
│   └── tasks.py        # Tarefas do Celery
├── tests/              # Testes automatizados
└── venv/               # Ambiente virtual Python
```

### Frontend (React)

```
frontend/
├── public/             # Arquivos estáticos
├── src/
│   ├── components/     # Componentes React
│   │   ├── auth/       # Componentes de autenticação
│   │   ├── layout/     # Componentes de layout
│   │   └── tasks/      # Componentes de tarefas
│   ├── contexts/       # Contextos React
│   ├── App.js          # Componente principal
│   └── index.js        # Ponto de entrada
├── tests/              # Testes automatizados
└── package.json        # Dependências
```

## Backend

### Modelos de Dados

#### User (models/user.py)

Representa um usuário no sistema.

**Campos:**
- `id`: Identificador único
- `name`: Nome do usuário
- `email`: Email do usuário (único)
- `hashed_password`: Senha criptografada
- `created_at`: Data de criação
- `updated_at`: Data de atualização

#### Task (models/task.py)

Representa uma tarefa no sistema.

**Campos:**
- `id`: Identificador único
- `title`: Título da tarefa
- `description`: Descrição da tarefa
- `due_date`: Data limite
- `priority`: Prioridade (baixa, media, alta)
- `status`: Status (pendente, em_andamento, concluida)
- `created_at`: Data de criação
- `updated_at`: Data de atualização
- `user_id`: ID do usuário proprietário
- `user`: Relacionamento com o usuário

### Schemas

#### User Schemas (schemas/user.py)

- `UserBase`: Schema base para usuários
- `UserCreate`: Schema para criação de usuários
- `UserResponse`: Schema para resposta de usuários

#### Task Schemas (schemas/task.py)

- `TaskBase`: Schema base para tarefas
- `TaskCreate`: Schema para criação de tarefas
- `TaskUpdate`: Schema para atualização de tarefas
- `TaskResponse`: Schema para resposta de tarefas

### Rotas

#### Autenticação (routes/auth.py)

- `POST /register`: Registra um novo usuário
- `POST /login`: Autentica um usuário e retorna um token JWT

#### Tarefas (routes/tasks.py)

- `GET /tasks`: Lista todas as tarefas do usuário
- `GET /tasks/{task_id}`: Obtém uma tarefa específica
- `POST /tasks`: Cria uma nova tarefa
- `PUT /tasks/{task_id}`: Atualiza uma tarefa existente
- `DELETE /tasks/{task_id}`: Exclui uma tarefa

### Operações CRUD

#### User CRUD (crud/user.py)

- `get_user_by_email`: Busca um usuário pelo email
- `get_user_by_id`: Busca um usuário pelo ID
- `create_user`: Cria um novo usuário
- `authenticate_user`: Autentica um usuário

#### Task CRUD (crud/task.py)

- `get_tasks`: Busca tarefas com filtros opcionais
- `get_task`: Busca uma tarefa específica
- `create_task`: Cria uma nova tarefa
- `update_task`: Atualiza uma tarefa existente
- `delete_task`: Exclui uma tarefa

### Utilitários

#### Autenticação (utils/auth.py)

- `verify_password`: Verifica se a senha corresponde ao hash
- `get_password_hash`: Gera um hash da senha
- `create_access_token`: Cria um token JWT

#### Dependências (utils/deps.py)

- `get_current_user`: Obtém o usuário atual a partir do token JWT

### Sistema de Notificações

#### Configuração do Celery (celery_app.py)

Configura o Celery para executar tarefas periódicas.

#### Tarefas do Celery (tasks.py)

- `check_task_deadlines`: Verifica tarefas com prazo próximo e envia notificações
- `send_email_notification`: Envia um email usando SendGrid

## Frontend

### Contextos

#### Autenticação (contexts/AuthContext.js)

Gerencia o estado de autenticação do usuário.

**Funções:**
- `login`: Autentica um usuário
- `register`: Registra um novo usuário
- `logout`: Desconecta o usuário

### Componentes

#### Autenticação

- `Login.js`: Formulário de login
- `Register.js`: Formulário de registro
- `ProtectedRoute.js`: Protege rotas que requerem autenticação

#### Layout

- `Header.js`: Barra de navegação superior

#### Tarefas

- `TaskList.js`: Lista de tarefas com filtros e ordenação
- `TaskForm.js`: Formulário para criação e edição de tarefas

## Fluxo de Dados

1. O usuário se registra ou faz login através dos formulários de autenticação
2. O backend valida as credenciais e retorna um token JWT
3. O frontend armazena o token e o utiliza para autenticar requisições subsequentes
4. O usuário pode criar, visualizar, atualizar e excluir tarefas
5. O sistema de notificações verifica diariamente as tarefas com prazo próximo e envia emails de lembrete

## Tecnologias Utilizadas

### Backend
- FastAPI: Framework web
- SQLAlchemy: ORM
- PostgreSQL: Banco de dados
- Pydantic: Validação de dados
- JWT: Autenticação
- Celery: Tarefas assíncronas
- Redis: Broker para Celery
- SendGrid: Envio de emails

### Frontend
- React: Biblioteca UI
- React Router: Navegação
- Material-UI: Componentes de interface
- Axios: Cliente HTTP
- Context API: Gerenciamento de estado
