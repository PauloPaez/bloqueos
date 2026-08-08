# scripts/models/personas.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class Personas(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    dni: Optional[str] = Field(default=None)
    nombre: Optional[str] = Field(default=None)
    apellido: Optional[str] = Field(default=None)
    empresa_cnx: Optional[str] = Field(default=None)
    login_cnx: Optional[str] = Field(default=None)
    calle_nro: Optional[str] = Field(default=None)
    barrio: Optional[str] = Field(default=None)
    departamento: Optional[str] = Field(default=None)
    provincia: Optional[str] = Field(default=None)
    cargo: Optional[str] = Field(default=None)
    login: Optional[str] = Field(default=None)
    empresa: Optional[str] = Field(default=None)
    activo: Optional[bool] = Field(default=False)
  