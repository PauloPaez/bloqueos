from pydantic import BaseModel, Field
from typing import Optional, Any

class Rutas(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    rol: Optional[str] = Field(default=None)
    componente: Optional[str] = Field(default=None)
    path: Optional[str] = Field(default=None)
    app: Optional[bool] = Field(default=False)
