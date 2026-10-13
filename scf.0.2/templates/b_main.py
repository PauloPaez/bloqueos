from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from scripts.routers.usuarios import usuarios
from scripts.routers.roles import roles
from scripts.routers.login import login
from scripts.routers.rutas import rutas
from scripts.routers.notificaciones import notificaciones
from scripts.routers.secuenciador import secuencia
from scripts.routers.generadorQR import DIRECTORIO_QR, generador_qr
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

DIRECTORIO_QR.mkdir(parents=True, exist_ok=True)
app.mount("/codigosQR", StaticFiles(directory=str(DIRECTORIO_QR)), name="codigosQR")

# AGREGAR ESTOS LOGS PARA DEBUG:
try:
    from scripts.routers.usuarios import usuarios
    logger.info("✅ Router usuarios importado correctamente")
except Exception as e:
    logger.error(f"❌ Error importando usuarios: {e}")

# try:
#     from scripts.routers.mercado_pago import mercado_pago
#     logger.info("✅ Router mercado_pago importado correctamente")
# except Exception as e:
#     logger.error(f"❌ Error importando mercado_pago: {e}")

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://techiar.cloud",

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
    try:
        init_db()
        logger.info("✅ MongoDB inicializado")        
        await redis_manager.initialize()
        # Iniciar listener de Redis en segundo plano
        asyncio.create_task(start_redis_listener())
        logger.info("Aplicación iniciada con Redis para WebSockets")
    except Exception as e:
        logger.error(f"Error en startup: {e}")


@app.websocket("/ws/{entity}")
async def websocket_endpoint(websocket: WebSocket, entity: str):
    valid_entities = [
        "usuarios", "roles", "login", "rutas", "personas","productos", 
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
app.include_router(notificaciones, tags=["Notificaciones"])
app.include_router(secuencia, tags=["Secuenciador"])
app.include_router(generador_qr, tags=["Generador QR"])


