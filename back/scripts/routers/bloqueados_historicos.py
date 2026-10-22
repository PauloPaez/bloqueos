from fastapi import APIRouter, HTTPException, Query
from scripts.querys.bloqueados_historicos import listar_periodos_historicos, consultar_bloqueados_historicos
from scripts.schemas.bloqueados_historicos import PeriodosHistoricosResponse, BloqueadosHistoricosResponse


bloqueados_historicos = APIRouter(prefix="/bloqueados-historicos")


@bloqueados_historicos.get("/", response_model=PeriodosHistoricosResponse)
async def listar_periodos(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)): #este consulta a la coleccion Habilitaciones
    try:
        return await listar_periodos_historicos(page, page_size)
    except Exception as e:
        print(f"ERROR al consultar los períodos históricos: {e}")
        raise HTTPException(status_code=500, detail="No se pudieron consultar los períodos históricos.")


@bloqueados_historicos.get("/{habilitacion_id}/", response_model=BloqueadosHistoricosResponse) #este consulta a BloqueadosHistoricos
async def consultar_periodo(habilitacion_id: str, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    try:
        resultado = await consultar_bloqueados_historicos(habilitacion_id, page, page_size)
        if resultado is None:
            raise HTTPException(status_code=404, detail="No se encontró un histórico confirmado para ese cierre.")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR al consultar los bloqueados históricos: {e}")
        raise HTTPException(status_code=500, detail="No se pudieron consultar los bloqueados históricos.")
