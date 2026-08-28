from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class Motivos(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    motivo: Optional[str] = Field(default=None)
    lleva_fecha: bool = Field(default=False)
    login: Optional[str] = Field(default=None)
    empresa: Optional[str] = Field(default=None)
    activo: Optional[bool] = Field(default=False)

    @field_validator('*', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
