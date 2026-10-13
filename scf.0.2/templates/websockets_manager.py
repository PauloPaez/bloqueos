from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict

# Gestión de conexiones activas clasificadas por entidad
active_connections: Dict[str, List[WebSocket]] = {
"rutas": [],
"roles": [],
"usuarios": [],
}

async def notify_clients(entity: str, message: str):
    """Notifica a todos los clientes conectados a una entidad específica."""
    if entity in active_connections:
        for connection in active_connections[entity]:
            try:
                await connection.send_text(message)
            except Exception:
                # Manejar errores de envío, como desconexión inesperada
                active_connections[entity].remove(connection)

async def add_connection(entity: str, websocket: WebSocket):
    """Agrega una conexión de WebSocket a una entidad específica."""
    if entity in active_connections:
        active_connections[entity].append(websocket)

async def remove_connection(entity: str, websocket: WebSocket):
    """Elimina una conexión de WebSocket de una entidad específica."""
    if entity in active_connections and websocket in active_connections[entity]:
        active_connections[entity].remove(websocket)
