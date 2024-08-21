from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Crear el motor (engine)
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Crear una clase de sesión
SessionLocal = sessionmaker(bind=engine)

# Definir la base declarativa
Base = declarative_base()

# Definir la clase Conversation
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    message = Column(String)
    response = Column(String)

# Crear la base de datos y las tablas
Base.metadata.create_all(engine)

