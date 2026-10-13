import sys

DB = sys.argv[1].upper()

conexion = f"""from motor.motor_asyncio import AsyncIOMotorClient
cliente = AsyncIOMotorClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/{DB}?retryWrites=true&w=majority')
database = cliente.{DB}
"""

print(conexion)

