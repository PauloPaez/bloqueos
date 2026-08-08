from pydantic import BaseModel, Field
from typing import Optional, Any

class Roles(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    rol: Optional[str] = Field(default=None)
    descripcion: Optional[str] = Field(default=None)
    activo: Optional[bool] = Field(default=False)
