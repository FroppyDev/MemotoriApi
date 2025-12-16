from sqlalchemy import Float, BigInteger, Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    nombre = Column(String, nullable=False)
    userId = Column(Integer, ForeignKey("users.id"), nullable=False)
    descripcion = Column(String, nullable=False)
    imagen = Column(String, nullable=True)
    color = Column(String, default="MORADO")
    smart = Column(Boolean, default=False)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    radioMetros = Column(Integer, nullable=True)
    tarjetas = relationship("Tarjeta", backref="categoria", cascade="all, delete")


class Tarjeta(Base):
    __tablename__ = "tarjeta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id"), nullable=False)
    idCategoria = Column(Integer, ForeignKey("categoria.id", ondelete="CASCADE"))
    concepto = Column(String, nullable=True)
    definicion = Column(String, nullable=True)
    definicionExtra = Column(String, nullable=True)
    imagen = Column(String, nullable=True)

class Horarios(Base):
    __tablename__ = "horarios"

    idHorario = Column(Integer, primary_key=True, autoincrement=True)
    idCategoria = Column(Integer, ForeignKey("categoria.id", ondelete="CASCADE"))
    userId = Column(Integer, ForeignKey("users.id"))
    horaInicio = Column(String, nullable=False)
    horaFin = Column(String, nullable=False)

class Dias(Base):
    __tablename__ = "dias"

    idDia = Column(Integer, primary_key=True)
    nombreDia = Column(String, nullable=False)

class CategoriaDias(Base):
    __tablename__ = "categoria_dias"

    idCategoria = Column(Integer, ForeignKey("categoria.id", ondelete="CASCADE"), primary_key=True)
    userId = Column(Integer, ForeignKey("users.id"))
    idDia = Column(Integer, ForeignKey("dias.idDia", ondelete="CASCADE"), primary_key=True)

class Imagenes(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    idCategoria = Column(Integer, ForeignKey("categoria.id", ondelete="CASCADE"))
    userId = Column(Integer, ForeignKey("users.id"))
    imagen = Column(String, nullable=False)
    infoImagen = Column(String, nullable=True)

class Fotos(Base):
    __tablename__ = "fotos"

    idFoto = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id"))
    rutaFoto = Column(String, nullable=False)
    fechaHora = Column(String, nullable=False)
    idCategoria = Column(Integer, ForeignKey("categoria.id", ondelete="CASCADE"))
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)