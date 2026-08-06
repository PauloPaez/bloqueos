# Desarrollo
from pathlib import Path
from dotenv import load_dotenv
# Fin Bloque Desarrollo
load_dotenv(Path(__file__).parent / ".env")
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from scripts.routers.escuelas import escuelas
from scripts.routers.login import login
from scripts.routers.notificaciones import notificaciones
from scripts.routers.personas import personas
from scripts.routers.roles import roles
from scripts.routers.rutas import rutas
from scripts.routers.usuarios import usuarios
from scripts.routers.motivos import motivos
from scripts.conf.engine import init_db, close_db

from utils.websockets_manager import (
    add_connection, 
    remove_connection, 
    notify_clients,
    redis_manager,
    start_redis_listener
)
import asyncio
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://10.66.181.153:5173",
    "http://localhost:5173",
    "https://testbloqueos.sanjuan.gob.ar",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Inicializar Redis, MongoDB y el listener al arrancar la aplicación"""
    init_db()
    logger.info("✅ MongoDB inicializado")

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
        "motivos",
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

@app.on_event("shutdown")
async def shutdown_event():
    close_db()
    logger.info("🔌 Conexión MongoDB cerrada")
    # Si redis_manager tiene close, también llamarlo
    if hasattr(redis_manager, "close"):
        await redis_manager.close()        
        

app.include_router(usuarios, tags=["Usuarios"])
app.include_router(roles, tags=["Roles"])
app.include_router(login, tags=["Login"])
app.include_router(rutas, tags=["Rutas"])
app.include_router(personas, tags=["Personas"])
app.include_router(notificaciones, tags=["Notificaciones"])
logger.info("✅ Router notificaciones incluido en la aplicación")
app.include_router(escuelas, tags=["Escuelas"])
app.include_router(motivos, tags=["Motivos"])