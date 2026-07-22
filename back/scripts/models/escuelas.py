from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class Escuelas(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    bloqueo: Optional[bool] = Field(default=False)
    tipo_reg: Optional[str] = Field(default=None)
    codigo_liquidacion: Optional[str] = Field(default=None)
    centro_pago: Optional[str] = Field(default=None)
    fecha_pago: Optional[datetime] = Field(default=None)
    sucursal_acreditacion: Optional[str] = Field(default=None)
    importe_acreditar: Optional[str] = Field(default=None)
    ayn: Optional[str] = Field(default=None)
    tipoynumdoc: Optional[str] = Field(default=None)
    sucursal_cuenta_digitodebito: Optional[str] = Field(default=None)
    cuil: Optional[str] = Field(default=None)
    zona: Optional[str] = Field(default=None)
    centro_sector: Optional[str] = Field(default=None)
    padron_digitoverificador: Optional[str] = Field(default=None)
    codigo_banco: Optional[str] = Field(default=None)
    motivo: Optional[str] = Field(default=None)
    fuente: Optional[str] = Field(default=None)
    login: Optional[str] = Field(default=None)
    empresa: Optional[str] = Field(default=None)
    activo: Optional[bool] = Field(default=False)

    @field_validator('*', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
