import os
from motor.motor_asyncio import AsyncIOMotorClient

_client = None
database = None


def init_db():
    global _client, database

    # Evita crear una nueva conexión si ya está inicializada
    if database is not None:
        return database

    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")

    if not uri:
        raise RuntimeError("No está definida la variable de entorno MONGO_URI")

    if not db_name:
        raise RuntimeError("No está definida la variable de entorno MONGO_DB")

    _client = AsyncIOMotorClient(uri)
    database = _client[db_name]

    return database


def close_db():
    global _client, database

    if _client:
        _client.close()

    _client = None
    database = None


def get_collection(name: str):
    if database is None:
        raise RuntimeError("Base de datos no inicializada. ¿Olvidaste llamar a init_db()?")

    return database[name]

# from motor.motor_asyncio import AsyncIOMotorClient
# cliente = AsyncIOMotorClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/BLOQUEOS_DPI?retryWrites=true&w=majority')
# database = cliente.BLOQUEOS_DPI



