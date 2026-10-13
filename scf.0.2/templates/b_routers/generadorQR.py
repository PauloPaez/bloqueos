# routers/generadorQR.py
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException
import json
import qrcode

generador_qr = APIRouter()
DIRECTORIO_QR = Path(__file__).resolve().parents[3] / "codigosQR"


@generador_qr.post("/generar_qr/")
async def generar_qr(datos: dict = Body(...)):
    if not datos:
        raise HTTPException(status_code=400, detail="Debe enviar un JSON con datos")

    datos_json = json.dumps(datos, ensure_ascii=False)
    nombre_archivo = f"qr_{uuid4().hex}.png"
    ruta_archivo = DIRECTORIO_QR / nombre_archivo

    try:
        DIRECTORIO_QR.mkdir(parents=True, exist_ok=True)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(datos_json)
        qr.make(fit=True)

        imagen_qr = qr.make_image(fill_color="black", back_color="white")
        imagen_qr.save(ruta_archivo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar QR: {e}")

    return {
        "mensaje": "Código QR generado exitosamente",
        "archivo": nombre_archivo,
        "ruta": str(ruta_archivo),
        "url": f"codigosQR/{nombre_archivo}",
        "datos": datos,
    }
