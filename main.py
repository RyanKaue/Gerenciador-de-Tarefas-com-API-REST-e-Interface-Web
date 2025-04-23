from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, tasks
from app.database import engine, Base
from app.celery_app import celery_app

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="Gerenciador de Tarefas API",
    description="API REST para gerenciamento de tarefas com autenticação JWT",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth.router)
app.include_router(tasks.router)

# Disponibilizar o app Celery
app.celery_app = celery_app

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Gerenciador de Tarefas"}

# Para iniciar o servidor: uvicorn main:app --reload
