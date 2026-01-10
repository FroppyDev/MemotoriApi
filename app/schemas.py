from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id:int
    is_active:bool
    created_at:datetime
    
    model_config = ConfigDict(from_attributes=True)


#//////////////////////////////////////////////////////////////

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    color: Optional[str] = "MORADO"
    smart: Optional[bool] = False
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    radioMetros: Optional[int] = None

class CrearCategoria(CategoriaBase):
    pass

class ActualizarCategoria(CategoriaBase):
    pass

class EliminarCategoria(BaseModel):
    id:int
    userId:int

class Categoria(CategoriaBase):
    id: int
    userId: int

    model_config = ConfigDict(from_attributes=True)


class ListaCategoria(BaseModel):
    categorias: List[Categoria]

#//////////////////////////////////////////////////////////////

# ---------- Card BASE ----------
class TarjetaBase(BaseModel):
    concepto: Optional[str]
    definicion: Optional[str]
    definicionExtra: Optional[str]
    imagen: Optional[str] = None

class TarjetaCreate(TarjetaBase):
    pass

class TarjetaUpdate(TarjetaBase):
    pass

class Tarjeta(TarjetaBase):
    id: int
    userId: int
    
    model_config = ConfigDict(from_attributes=True)


#//////////////////////////////////////////////////////////////