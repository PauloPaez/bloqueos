from pydantic import BaseModel, Field
from typing import Optional, Any
  
class Usuarios(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    nombre: Optional[str] = Field(default=None)
    apellido: Optional[str] = Field(default=None)
    empresas: Optional[list[str]] = Field(default=[])
    
    dni: Optional[str] = Field(default=None)
    calle_nro: Optional[str] = Field(default=None)
    barrio: Optional[str] = Field(default=None)
    departamento: Optional[str] = Field(default=None)
    provincia: Optional[str] = Field(default=None)
    cargo: Optional[str] = Field(default=None)
    
    login: Optional[str] = Field(default=None)
    clave: Optional[str] = Field(default=None)
    roles: Optional[list[str]] = Field(default=[])  # Cambiado a lista de cadenas
    activo: Optional[bool] = Field(default=False)
