# API do Gerenciador de Tarefas

## Visão Geral

Esta documentação descreve a API REST do Gerenciador de Tarefas, uma aplicação para gerenciamento de tarefas com autenticação JWT, desenvolvida com FastAPI.

## Base URL

```
http://localhost:8000
```

## Autenticação

A API utiliza autenticação JWT (JSON Web Token). Para acessar endpoints protegidos, é necessário incluir o token no cabeçalho de autorização:

```
Authorization: Bearer {seu_token_jwt}
```

Para obter um token, utilize o endpoint de login.

## Endpoints

### Autenticação

#### Registro de Usuário

```
POST /register
```

Registra um novo usuário no sistema.

**Corpo da Requisição:**
```json
{
  "name": "Nome do Usuário",
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

**Resposta (201 Created):**
```json
{
  "id": 1,
  "name": "Nome do Usuário",
  "email": "usuario@exemplo.com",
  "created_at": "2025-04-22T14:30:00.000Z"
}
```

#### Login

```
POST /login
```

Autentica um usuário e retorna um token JWT.

**Corpo da Requisição (form-data):**
```
username: usuario@exemplo.com
password: senha123
```

**Resposta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Tarefas

#### Listar Tarefas

```
GET /tasks
```

Retorna todas as tarefas do usuário autenticado.

**Parâmetros de Consulta (opcionais):**
- `status`: Filtrar por status (pendente, em_andamento, concluida)
- `priority`: Filtrar por prioridade (baixa, media, alta)
- `due_date_before`: Filtrar por data limite (formato ISO)
- `order_by`: Ordenar por campo (created_at, due_date, priority, status)
- `order_direction`: Direção da ordenação (asc, desc)
- `skip`: Número de registros para pular (paginação)
- `limit`: Número máximo de registros a retornar (paginação)

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Exemplo de Tarefa",
    "description": "Descrição da tarefa",
    "due_date": "2025-04-23T14:30:00.000Z",
    "priority": "media",
    "status": "pendente",
    "created_at": "2025-04-22T14:30:00.000Z",
    "updated_at": null,
    "user_id": 1
  }
]
```

#### Obter Tarefa Específica

```
GET /tasks/{task_id}
```

Retorna uma tarefa específica do usuário autenticado.

**Resposta (200 OK):**
```json
{
  "id": 1,
  "title": "Exemplo de Tarefa",
  "description": "Descrição da tarefa",
  "due_date": "2025-04-23T14:30:00.000Z",
  "priority": "media",
  "status": "pendente",
  "created_at": "2025-04-22T14:30:00.000Z",
  "updated_at": null,
  "user_id": 1
}
```

#### Criar Tarefa

```
POST /tasks
```

Cria uma nova tarefa para o usuário autenticado.

**Corpo da Requisição:**
```json
{
  "title": "Nova Tarefa",
  "description": "Descrição da nova tarefa",
  "due_date": "2025-04-23T14:30:00.000Z",
  "priority": "alta",
  "status": "pendente"
}
```

**Resposta (201 Created):**
```json
{
  "id": 2,
  "title": "Nova Tarefa",
  "description": "Descrição da nova tarefa",
  "due_date": "2025-04-23T14:30:00.000Z",
  "priority": "alta",
  "status": "pendente",
  "created_at": "2025-04-22T15:00:00.000Z",
  "updated_at": null,
  "user_id": 1
}
```

#### Atualizar Tarefa

```
PUT /tasks/{task_id}
```

Atualiza uma tarefa existente do usuário autenticado.

**Corpo da Requisição:**
```json
{
  "title": "Tarefa Atualizada",
  "status": "em_andamento"
}
```

**Resposta (200 OK):**
```json
{
  "id": 2,
  "title": "Tarefa Atualizada",
  "description": "Descrição da nova tarefa",
  "due_date": "2025-04-23T14:30:00.000Z",
  "priority": "alta",
  "status": "em_andamento",
  "created_at": "2025-04-22T15:00:00.000Z",
  "updated_at": "2025-04-22T15:30:00.000Z",
  "user_id": 1
}
```

#### Excluir Tarefa

```
DELETE /tasks/{task_id}
```

Exclui uma tarefa do usuário autenticado.

**Resposta (200 OK):**
```json
{
  "id": 2,
  "title": "Tarefa Atualizada",
  "description": "Descrição da nova tarefa",
  "due_date": "2025-04-23T14:30:00.000Z",
  "priority": "alta",
  "status": "em_andamento",
  "created_at": "2025-04-22T15:00:00.000Z",
  "updated_at": "2025-04-22T15:30:00.000Z",
  "user_id": 1
}
```

## Códigos de Status

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Requisição inválida
- `401 Unauthorized`: Autenticação necessária
- `404 Not Found`: Recurso não encontrado
- `422 Unprocessable Entity`: Erro de validação

## Sistema de Notificações

O sistema inclui um serviço de notificações por e-mail que envia lembretes 24 horas antes do prazo das tarefas. Este serviço é executado automaticamente através do Celery e Redis, não sendo necessário chamar nenhum endpoint específico para ativá-lo.
