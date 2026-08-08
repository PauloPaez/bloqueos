import asyncio
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from scripts.routers.escuelas import escuelas
from scripts.routers.generacionDocs import routerDocs
from scripts.routers.login import login
from scripts.routers.notificaciones import notificaciones
from scripts.routers.personas import personas
from scripts.routers.roles import roles
from scripts.routers.rutas import rutas
from scripts.routers.usuarios import usuarios
from utils.websockets_manager import (
    add_connection,
    notify_clients,
    redis_manager,
    remove_connection,
    start_redis_listener,
)

logger = logging.getLogger(__name__)
app = FastAPI()
# AGREGAR ESTOS LOGS PARA DEBUG:
try:
    from scripts.routers.usuarios import usuarios

    logger.info("✅ Router usuarios importado correctamente")
except Exception as e:
    logger.error(f"❌ Error importando usuarios: {e}")
origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://lab.techiar.cloud",
    "https://subasta.techiar.cloud",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "Content-Disposition"
    ],  # si hay problemas en prod por archivos, podria ser por esto, pero muy dificil que sea esa la causa. Ya que solo le muestra el nombre del archivo generado por el backend. Ya que si no esta esto, el nombre va a ser el de la variable nombrePorDefecto definida al llamar al helper de descargarArchivo en javascrpit
)


@app.on_event("startup")
async def startup_event():
    """Inicializar Redis y el listener al arrancar la aplicación"""
    try:
        await redis_manager.initialize()
        # Iniciar listener de Redis en segundo plano
        asyncio.create_task(start_redis_listener())
        logger.info("Aplicación iniciada con Redis para WebSockets")
    except Exception as e:
        logger.error(f"Error en startup: {e}")


@app.websocket("/ws/{entity}")
async def websocket_endpoint(websocket: WebSocket, entity: str):
    valid_entities = [
        "usuarios",
        "roles",
        "login",
        "rutas",
        "personas",
        "escuelas",
    ]
    if entity not in valid_entities:
        await websocket.close()
        return
    await websocket.accept()
    await add_connection(entity, websocket)
    try:
        while True:
            # Mantener la conexión activa
            data = await websocket.receive_text()
            # Opcional: procesar mensajes entrantes del cliente si es necesario
            # await handle_client_message(entity, data)
    except WebSocketDisconnect:
        await remove_connection(entity, websocket)
    except Exception as e:
        logger.error(f"Error en WebSocket {entity}: {e}")
        await remove_connection(entity, websocket)


app.include_router(usuarios, tags=["Usuarios"])
app.include_router(roles, tags=["Roles"])
app.include_router(login, tags=["Login"])
app.include_router(rutas, tags=["Rutas"])
app.include_router(personas, tags=["Personas"])
app.include_router(notificaciones, tags=["Notificaciones"])
logger.info("✅ Router notificaciones incluido en la aplicación")
app.include_router(escuelas, tags=["Escuelas"])
app.include_router(routerDocs)
