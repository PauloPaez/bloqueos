from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class Motivos(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    concepto: Optional[str] = Field(default=None)
    login: Optional[str] = Field(default=None)
    empresa: Optional[str] = Field(default=None)
    activo: Optional[bool] = Field(default=False)

    @field_validator('*', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
