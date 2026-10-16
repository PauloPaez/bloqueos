from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator, model_validator
from utils.padrones.importPadron import ordenar_periodo


def normalizar_periodo(periodo: str) -> str:
    ordenar_periodo(periodo) #esta funcion verifica si el periodo ingresado corresponde a lo que espera el sistema
    return periodo.upper().replace("SEPTIEMBRE", "SETIEMBRE") #si el user envia Septiembre lo convierte a lo que espera el sistema


class HabilitacionesBase(BaseModel):
    rol: str | None = Field(default=None)
    periodo: str | None = Field(default=None)
    fecha_cierre: datetime | None = Field(default=None)
    cerrado: bool | None = Field(default=False)
    login: str | None = Field(default=None)
    empresa: str | None = Field(default=None)
    activo: bool | None = Field(default=False)

    @field_validator('*', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class HabilitacionesEntrada(HabilitacionesBase): #esto lo hice ya que el response tambien validaba el periodo, rompiendo el listado y no habia posibilidad de ver un error y desactivarlo
    """Comparte las validaciones de entrada entre creación y actualización."""

    @field_validator("periodo")
    @classmethod
    def validar_periodo(cls, value):
        return normalizar_periodo(value) if value is not None else None

    @field_validator("fecha_cierre")
    @classmethod
    def validar_fecha_cierre(cls, value):
        # Es una fecha de calendario: hoy es válido, sin comparar la hora de cierre.
        hoy = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).date()
        if value is not None and value.date() < hoy:
            raise ValueError("La fecha de cierre no puede ser anterior a hoy.")
        return value


class HabilitacionesCreate(HabilitacionesEntrada):
    rol: str
    periodo: str
    cerrado: Literal[False] = False  # Toda habilitación se crea abierta; el cierre es manual.

    @field_validator("cerrado", mode="before")
    @classmethod
    def normalizar_cerrado(cls, value):
        return False if value is None else value


class HabilitacionesResponse(HabilitacionesBase):
    rol: str
    id: str  # ID del documento


class HabilitacionesUpdate(HabilitacionesEntrada):
    id: str

    @model_validator(mode="before")
    @classmethod
    def omitir_cerrado_nulo(cls, data):
        # null no solicita cambiar el estado; solo true o false lo modifican.
        if isinstance(data, dict) and data.get("cerrado") is None:
            return {campo: valor for campo, valor in data.items() if campo != "cerrado"}
        return data

    @model_validator(mode="after")
    def validar_periodo_enviado(self):
        if "periodo" in self.model_fields_set and self.periodo is None:
            raise ValueError("El período debe tener formato MESAA.")
        return self

