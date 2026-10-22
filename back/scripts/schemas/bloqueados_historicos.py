from datetime import datetime
from typing import Any
from pydantic import BaseModel


class PeriodoHistorico(BaseModel):
    id: str
    periodo: str
    fecha_cierre_real: datetime
    cantidad_bloqueadas: int


class PeriodosHistoricosResponse(BaseModel):
    data: list[PeriodoHistorico]
    total: int
    page: int
    page_size: int
    total_pages: int


class BloqueadosHistoricosResponse(BaseModel):
    periodo: str
    fecha_cierre_real: datetime
    data: list[dict[str, Any]]
    total: int
    page: int
    page_size: int
    total_pages: int
