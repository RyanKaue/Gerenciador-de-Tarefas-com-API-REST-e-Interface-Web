from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração da conexão com o banco de dados PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://taskmanager:taskmanager123@localhost/taskmanagerdb"

# Criação do engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
