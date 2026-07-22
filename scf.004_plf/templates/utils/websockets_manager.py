# utils/websockets_manager.py
import json
import asyncio
# import redis.asyncio as redis
from fastapi import WebSocket
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Configuración de Redis
REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "decode_responses": True,
    "encoding": "utf-8"
}

class RedisManager:
    _instance = None
    _redis_client = None
    _pubsub = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisManager, cls).__new__(cls)
        return cls._instance
    
    async def initialize(self):
        """Inicializar conexión a Redis"""
        try:
            self._redis_client = redis.Redis(**REDIS_CONFIG)
            self._pubsub = self._redis_client.pubsub()
            
            # Suscribirse a todos los canales de entidades
            entities = ["usuarios", "roles", "login", "rutas","personas","pedidos","ofertas",]
            for entity in entities:
                await self._pubsub.subscribe(f"ws_{entity}")
                
            logger.info("Redis Manager inicializado correctamente")
        except Exception as e:
            logger.error(f"Error inicializando Redis: {e}")
            raise
    
    async def publish(self, entity: str, message: str):
        """Publicar mensaje a un canal específico"""
        if self._redis_client:
            await self._redis_client.publish(f"ws_{entity}", message)
    
    async def listen(self):
        """Escuchar mensajes de Redis"""
        async for message in self._pubsub.listen():
            if message['type'] == 'message':
                yield message

# Instancia global de Redis Manager
redis_manager = RedisManager()

# ----------------------Gestión de conexiones activas locales por worker-------------------
active_connections: Dict[str, List[WebSocket]] = {
    "pedidos": [],
    "ofertas": [],
    "personas": [],
}

async def start_redis_listener():
    """Iniciar el listener de Redis en segundo plano"""
    try:
        async for message in redis_manager.listen():
            channel = message['channel']
            data = message['data']
            
            # Extraer la entidad del canal (ws_entidad -> entidad)
            entity = channel.replace('ws_', '')
            
            if entity in active_connections:
                # Enviar a todas las conexiones locales de esta entidad
                for connection in active_connections[entity][:]:  # Copia de la lista
                    try:
                        await connection.send_text(data)
                    except Exception as e:
                        # Remover conexión problemática
                        active_connections[entity].remove(connection)
                        logger.warning(f"Conexión removida: {e}")
                        
    except Exception as e:
        logger.error(f"Error en Redis listener: {e}")

async def notify_clients(entity: str, message: str):
    """Notifica a todos los clientes conectados a una entidad específica a través de todos los workers"""
    if entity in active_connections:
        # Primero notificar a las conexiones locales
        for connection in active_connections[entity][:]:  # Copia de la lista
            try:
                print('enviando mensaje: ', message)
                await connection.send_text(message)
            except Exception:
                # Remover conexión problemática
                active_connections[entity].remove(connection)
        
        # Luego publicar en Redis para otros workers
        try:
            await redis_manager.publish(entity, message)
        except Exception as e:
            logger.error(f"Error publicando en Redis: {e}")

async def add_connection(entity: str, websocket: WebSocket):
    """Agrega una conexión de WebSocket a una entidad específica"""
    if entity in active_connections:
        active_connections[entity].append(websocket)
        logger.info(f"Conexión agregada a {entity}. Total: {len(active_connections[entity])}")

async def remove_connection(entity: str, websocket: WebSocket):
    """Elimina una conexión de WebSocket de una entidad específica"""
    if entity in active_connections and websocket in active_connections[entity]:
        active_connections[entity].remove(websocket)
        logger.info(f"Conexión removida de {entity}. Total: {len(active_connections[entity])}")

