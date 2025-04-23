from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class PriorityEnum(enum.Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"

class StatusEnum(enum.Enum):
    pendente = "pendente"
    em_andamento = "em_andamento"
    concluida = "concluida"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime(timezone=True))
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.media)
    status = Column(Enum(StatusEnum), default=StatusEnum.pendente)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamento com o usuário
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="tasks")
