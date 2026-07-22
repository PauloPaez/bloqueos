from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://subasta:NWNBujJQwpbNRyAT@cluster0.v7trii7.mongodb.net/?appName=Cluster0"

cliente = AsyncIOMotorClient(
                                uri,
                                server_api=ServerApi("1")
    )
database = cliente["SUBASTAR"]


# from motor.motor_asyncio import AsyncIOMotorClient
# cliente = AsyncIOMotorClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/STOCKIAR?retryWrites=true&w=majority')
# database = cliente.STOCKIAR
