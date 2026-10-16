import unittest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from pydantic import ValidationError

from scripts.routers import habilitaciones as router
from scripts.schemas.schemaHabilitaciones import (
    HabilitacionesCreate,
    HabilitacionesResponse,
    HabilitacionesUpdate,
)


class HabilitacionesPeriodoTests(unittest.TestCase):
    def test_normaliza_periodo_en_creacion_y_actualizacion(self):
        self.assertEqual(
            HabilitacionesCreate(rol="Admin", periodo="septiembre26").periodo,
            "SETIEMBRE26",
        )
        self.assertEqual(
            HabilitacionesUpdate(id="123", rol="Admin", periodo="enero27").periodo,
            "ENERO27",
        )

    def test_rechaza_periodo_ausente_o_invalido(self):
        for periodo in (None, "", "MES26", "JUNIO2026", "../JUNIO26"):
            with self.subTest(periodo=periodo), self.assertRaises(ValidationError):
                HabilitacionesCreate(rol="Admin", periodo=periodo)
        with self.assertRaises(ValidationError):
            HabilitacionesCreate(rol="Admin")

    def test_actualizacion_puede_omitir_periodo_y_rol(self):
        item = HabilitacionesUpdate(id="123", fecha_cierre="2026-10-16")
        self.assertEqual(set(item.model_dump(exclude_unset=True)), {"id", "fecha_cierre"})

    def test_actualizacion_rechaza_periodo_invalido_si_se_envia(self):
        for periodo in (None, "", "MES26"):
            with self.subTest(periodo=periodo), self.assertRaises(ValidationError):
                HabilitacionesUpdate(id="123", periodo=periodo)

    def test_respuesta_admite_registros_historicos_sin_periodo(self):
        self.assertIsNone(HabilitacionesResponse(id="123", rol="Admin").periodo)

    def test_respuesta_no_valida_ni_normaliza_periodos_guardados(self):
        for periodo in ("123", "septiembre26", "MES26"):
            with self.subTest(periodo=periodo):
                respuesta = HabilitacionesResponse(id="123", rol="Admin", periodo=periodo)
                self.assertEqual(respuesta.periodo, periodo)


class HabilitacionesPatchPeriodoTests(unittest.IsolatedAsyncioTestCase):
    async def test_put_envia_solo_campos_informados(self):
        with patch.object(router, "put_habilitaciones", new_callable=AsyncMock) as guardar, \
                patch.object(router, "notify_clients", new_callable=AsyncMock):
            guardar.return_value = {"status": "success"}
            await router.update_habilitaciones(HabilitacionesUpdate(id="123", rol="Nueva área"))
            guardar.assert_awaited_once_with({"id": "123", "rol": "Nueva área"})

    async def test_patch_normaliza_periodo(self):
        with patch.object(router, "patch_habilitaciones", new_callable=AsyncMock) as guardar, \
                patch.object(router, "notify_clients", new_callable=AsyncMock):
            guardar.return_value = {"status": "success"}
            await router.partial_update_habilitaciones(
                HabilitacionesUpdate(id="123", periodo="septiembre26")
            )
            self.assertEqual(guardar.await_args.args[0]["periodo"], "SETIEMBRE26")

    async def test_patch_rechaza_periodo_invalido_antes_de_guardar(self):
        with patch.object(router, "patch_habilitaciones", new_callable=AsyncMock) as guardar:
            # FastAPI construye este schema antes de llamar al endpoint.
            with self.assertRaises(ValidationError):
                habilitacion = HabilitacionesUpdate(id="123", periodo="MES26")
                await router.partial_update_habilitaciones(habilitacion)
            guardar.assert_not_awaited()

    async def test_patch_conserva_error_400_sin_notificar(self):
        with patch.object(router, "patch_habilitaciones", new_callable=AsyncMock) as guardar, \
                patch.object(router, "notify_clients", new_callable=AsyncMock) as notificar:
            guardar.return_value = {"status": "failed", "message": "No se actualizó el documento"}
            with self.assertRaises(HTTPException) as error:
                await router.partial_update_habilitaciones(HabilitacionesUpdate(id="123", activo=False))
            self.assertEqual(error.exception.status_code, 400)
            self.assertEqual(error.exception.detail, "No se actualizó el documento")
            notificar.assert_not_awaited()

    async def test_patch_error_inesperado_devuelve_500_sin_detalles_internos(self):
        with patch.object(router, "patch_habilitaciones", new_callable=AsyncMock) as guardar, \
                patch.object(router, "notify_clients", new_callable=AsyncMock) as notificar:
            guardar.side_effect = RuntimeError("Detalle interno de prueba")
            with self.assertRaises(HTTPException) as error:
                await router.partial_update_habilitaciones(HabilitacionesUpdate(id="123", activo=False))
            self.assertEqual(error.exception.status_code, 500)
            self.assertNotIn("Detalle interno", error.exception.detail)
            notificar.assert_not_awaited()
