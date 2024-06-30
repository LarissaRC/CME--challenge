from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Material(Base):
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    tipo = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo
        }

class Etapa(Base):
    __tablename__ = 'etapa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome
        }

class Falha(Base):
    __tablename__ = 'falha'
    id = Column(Integer, primary_key=True)
    descricao = Column(Text, nullable=False)
    material_id = Column(Integer, ForeignKey('material.id'), nullable=False)
    etapa_id = Column(Integer, ForeignKey('etapa.id'), nullable=False)
    data_hora = Column(DateTime, nullable=False)

    material = relationship('Material', backref=backref('falhas', lazy=True))
    etapa = relationship('Etapa', backref=backref('falhas', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "material_id": self.material_id,
            "etapa_id": self.etapa_id,
            "data_hora": self.data_hora.isoformat()
        }

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('material.id'), nullable=False)
    etapa_id = Column(Integer, ForeignKey('etapa.id'), nullable=False)
    data_hora = Column(DateTime, nullable=False)

    material = relationship('Material', backref=backref('statuses', lazy=True))
    etapa = relationship('Etapa', backref=backref('statuses', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "material_id": self.material_id,
            "etapa_id": self.etapa_id,
            "data_hora": self.data_hora.isoformat()
        }
