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

## Autor

Desenvolvido por Manus AI
