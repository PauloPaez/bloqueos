from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from utils.formateoDatos import formatear_concepto, formatear_importe, _con_digito_verificador


def escuelasSh(item):
    importe_acreditado = item.get("importe_acreditado")

    return {
        "id": str(item.get("_id")),
        "concepto": formatear_concepto(
            item.get("tipo_archivo"), item.get("periodo")
        ),
        "bloqueo": item.get("bloqueo"),
        "tipo_reg": item.get("tipo_reg"),
        "cod_liquidacion": item.get("cod_liquidacion"),
        "centro_pago": item.get("centro_pago"),
        "pago_anio": item.get("pago_anio"),
        "pago_mes": item.get("pago_mes"),
        "pago_dia": item.get("pago_dia"),
        "suc_acreditacion": item.get("suc_acreditacion"),
        "tipo_acreditacion": item.get("tipo_acreditacion"),
        "cuenta_acreditacion": item.get("cuenta_acreditacion"),
        "cuenta_acreditacion_dv": item.get("cuenta_acreditacion_dv"),
        "importe_acreditado": importe_acreditado,
        "importe_acreditado_formateado": formatear_importe(importe_acreditado),
        "beneficiario_nombre": item.get("beneficiario_nombre"),
        "documento_tipo": item.get("documento_tipo"),
        "documento_nro": item.get("documento_nro"),
        "suc_debito": item.get("suc_debito"),
        "tipo_debito": item.get("tipo_debito"),
        "cuenta_debito": item.get("cuenta_debito"),
        "cuenta_debito_dv": item.get("cuenta_debito_dv"),
        "cuil": item.get("cuil"),
        "zona": item.get("zona"),
        "centro": item.get("centro"),
        "sector": item.get("sector"),
        "padron": item.get("padron"),
        "padron_dv": item.get("padron_dv"),
        "padron_formateado": _con_digito_verificador(item.get("padron"), item.get("padron_dv")),
        "reservado": item.get("reservado"),
        "cod_banco": item.get("cod_banco"),
        "tipo_archivo": item.get("tipo_archivo"),
        "periodo": item.get("periodo"),
        "motivo": item.get("motivo"),
        "fecha_baja": item.get("fecha_baja"),
        "login": item.get("login"),
        "empresa": item.get("empresa"),
        "activo": item.get("activo"),
    }


class EscuelasPatch(BaseModel):
    id: str = Field(..., description="ID del documento a actualizar")
    bloqueo: Optional[bool] = Field(default=None)
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
    bloquear_todos_padrones_dni: bool = Field(default=False)
    login: Optional[str] = Field(default=None)
    empresa: Optional[str] = Field(default=None)
    activo: Optional[bool] = Field(default=None)

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value
    @field_validator("fecha_baja", mode="before")
    @classmethod
    def convertir_fecha_baja(cls, value):
        if value in ("", None):
            return None

        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d")

        return value
