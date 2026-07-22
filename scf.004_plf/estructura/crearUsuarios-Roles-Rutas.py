# CREAR ADMINSITADOR , ROL ADMINISTRaDOR y RUTAS a los componentes Usuarios, Roles y Rutas.py
import json
from typing import Dict, Any
from pymongo import MongoClient, errors
import sys
from pathlib import Path
directorio_actual = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------------------
# Configuración de la conexión a MongoDB
client = MongoClient('mongodb+srv://paulo:Paulo2023@cluster0.prraayx.mongodb.net/COOP3?retryWrites=true&w=majority')
# Recibir nombre Base de Datos
DB =  sys.argv[1].upper()
database = client[DB] 

# ---------------------------------------------------------------------------------------
def agregar_usuario(login, empresas, roles, activo=True):
    """Agrega un usuario con una lista de roles."""
    coleccion_usuarios = database["Usuarios"]
    usuario = {"nombre": login,"apellido": login, "empresas": empresas , "login": login, "clave" : "!2E", "roles": roles, "activo": activo}
    try:
        coleccion_usuarios.insert_one(usuario)
        print("Usuario agregado correctamente.")
    except errors.DuplicateKeyError:
        print("Error: El usuario ya existe.")

def agregar_rol(rol, descripcion):
    """Agrega un usuario con una lista de roles."""
    coleccion_roles = database["Roles"]
    rol = {"rol": rol,"descripcion": descripcion, "activo": True}
    try:
        coleccion_roles.insert_one(rol)
        print("Rol agregado correctamente.")
    except errors.DuplicateKeyError:
        print("Error: El Rol ya existe.")
        
#------------------------------------------------------------------------------------------        
def rutas():
    coleccion_rutas = database["Rutas"]
    rutas_json = directorio_actual / "rutas.json"
    print(f"Importando Rutas desde: {rutas_json}")
    # 🔹 Leer archivo JSON
    with open(rutas_json, "r", encoding="utf-8") as f:
        datos = json.load(f)
        
    # Insertar documentos
    if datos:
        coleccion_rutas.insert_many(datos)
        print(f"Importadas {len(datos)} Rutas")
    else:
        print("El archivo está vacío")
    
#--------------------------------------------------------------------------------------------

# Recibir nombre Modelo
rutas()      
agregar_usuario("admin", ["Techiar"], ["Administrador"], True)        
agregar_rol("Administrador", "Administrador")
