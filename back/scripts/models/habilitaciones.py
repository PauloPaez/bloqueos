from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class Habilitaciones(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    rol: str | None
    periodo: Optional[str] = Field(default=None)
    fecha_cierre: Optional[datetime] = Field(default=None)
    cerrado: bool | None = Field(default=False)
    login: Optional[str] = Field(default=None)
    empresa: Optional[str] = Field(default=None)
    activo: Optional[bool] = Field(default=False)

    @field_validator('*', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
