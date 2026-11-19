from bson.objectid import ObjectId
# ----------------------------------------------------
from scripts.conf.engine import get_collection
from utils.claves import es_hash, hashear_clave, verificar_clave
# -----------------------------------------------------


async def get_login(datos):
    coleccionUsr = get_collection("Usuarios")
    coleccionRutas = get_collection("Rutas")
    try:
        app = datos.app
        # El filtro lo arma el servidor: el cliente no decide qué se busca ni si el usuario está activo
        filtro = {"login": datos.login, "activo": True}
        usuario = await coleccionUsr.find_one(filtro, {"clave": 1, "roles": 1, "empresas": 1})
        # La clave se compara acá y no dentro de la consulta a Mongo
        if usuario and verificar_clave(usuario.get("clave"), datos.clave):
            # Si la clave estaba en texto plano, se guarda hasheada (se migra en el primer login)
            if not es_hash(usuario["clave"]):
                await coleccionUsr.update_one(
                    {"_id": usuario["_id"]}, {"$set": {"clave": hashear_clave(datos.clave)}})
            roles = usuario.get("roles", [])
            # Buscar las rutas asociadas a los roles del usuario
            cursor = coleccionRutas.find({"rol": {"$in": roles}}, {
                "path": 1, "componente": 1, "_id": 0, "app": 1, "nombre": 1}).sort("path", 1)
            # Convertir el cursor en una lista
            rutas = await cursor.to_list(length=None)
            print("Rutas encontradas:", rutas)
            # Filtrar rutas basado en el valor de 'app' y eliminar el campo 'app'
            rutas_filtradas = [
                {"componente": ruta["componente"],
                    "path": ruta["path"], "nombre": ruta.get("nombre")}
                for ruta in rutas
                if ruta.get("app") == app
            ]

            resultado = {"opciones": rutas_filtradas}
            resultado["login"] = datos.login
            resultado["empresa"] = usuario["empresas"][0]
            resultado["id"] = str(usuario["_id"])
            return resultado  # Devuelve el resultado con las rutas filtradas
        else:
            print("Usuario no encontrado o inactivo.")
            # Devuelve una lista vacía si no se encuentra el usuario
            return {"opciones": [[{'componente': 'SinOpciones', 'path': '/Error/SinOpciones', 'nombre': 'Sin Opciones'}]]}
    except Exception as e:
        raise Exception(f"Error al buscar documentos: {e}")
