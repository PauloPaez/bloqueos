from bson.objectid import ObjectId
from typing import Dict, Any
# ----------------------------------------------------
from scripts.conf.engine import get_collection
# -----------------------------------------------------


async def get_login(filter: Dict[str, Any]):
    coleccionUsr = get_collection("Usuarios")
    coleccionRutas = get_collection("Rutas")
    try:
        app = filter["app"]
        del filter["app"]
        # Buscar el usuario
        print("Filtro de login:", filter)
        usuario = await coleccionUsr.find_one(filter, {"roles": 1, "empresas": 1})
        print("Usuario encontrado:", usuario)
        if usuario:
            roles = usuario.get("roles", [])
            # Buscar las rutas asociadas a los roles del usuario
            cursor = coleccionRutas.find({"rol": {"$in": roles}}, {
                "path": 1, "componente": 1, "_id": 0, "app": 1, "nombre": 1})
            # Convertir el cursor en una lista
            rutas = await cursor.to_list(length=None)
            print("Rutas encontradas:", rutas)
            # Filtrar rutas basado en el valor de 'app' y eliminar el campo 'app'
            rutas_filtradas = [
                {"componente": ruta["componente"],
                    "path": ruta["path"], "nombre": ruta["nombre"]}
                for ruta in rutas
                if ruta.get("app") == app
            ]

            resultado = {"opciones": rutas_filtradas}
            resultado["login"] = filter["login"]
            resultado["empresa"] = usuario["empresas"][0]
            resultado["id"] = str(usuario["_id"])
            return resultado  # Devuelve el resultado con las rutas filtradas
        else:
            print("Usuario no encontrado o inactivo.")
            # Devuelve una lista vacía si no se encuentra el usuario
            return {"opciones": [[{'componente': 'SinOpciones', 'path': '/Error/SinOpciones', 'nombre': 'Sin Opciones'}]]}
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")
