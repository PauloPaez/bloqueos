from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class Escuelas(BaseModel):
    id: Optional[str] = Field(default=None)  # ID del documento
    bloqueo: Optional[bool] = Field(default=False)
    tipo_reg: Optional[str] = Field(default=None)
    cod_liquidacion: Optional[str] = Field(default=None)
    centro_pago: Optional[str] = Field(default=None)
    pago_anio: Optional[str] = Field(default=None)
    pago_mes: Optional[str] = Field(default=None)
    pago_dia: Optional[str] = Field(default=None)
    suc_acreditacion: Optional[str] = Field(default=None)
    tipo_acreditacion: Optional[str] = Field(default=None)
    cuenta_acreditacion: Optional[str] = Field(default=None)
    cuenta_acreditacion_dv: Optional[str] = Field(default=None)
    importe_acreditado: Optional[str] = Field(default=None)
    beneficiario_nombre: Optional[str] = Field(default=None)
    documento_tipo: Optional[str] = Field(default=None)
    documento_nro: Optional[str] = Field(default=None)
    suc_debito: Optional[str] = Field(default=None)
    tipo_debito: Optional[str] = Field(default=None)
    cuenta_debito: Optional[str] = Field(default=None)
    cuenta_debito_dv: Optional[str] = Field(default=None)
    cuil: Optional[str] = Field(default=None)
    zona: Optional[str] = Field(default=None)
    centro: Optional[str] = Field(default=None)
    sector: Optional[str] = Field(default=None)
    padron: Optional[str] = Field(default=None)
    padron_dv: Optional[str] = Field(default=None)
    reservado: Optional[str] = Field(default=None)
    cod_banco: Optional[str] = Field(default=None)
    tipo_archivo: Optional[str] = Field(default=None)
    periodo: Optional[str] = Field(default=None)
    motivo: Optional[str] = Field(default=None)
    fecha_baja: datetime | None = Field(default=None)
    login: Optional[str] = Field(default=None)
    empresa: Optional[str] = Field(default=None)
    activo: Optional[bool] = Field(default=False)

    @field_validator('*', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
