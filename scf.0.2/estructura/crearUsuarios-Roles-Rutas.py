import json

from pathlib import Path
from database import database


directorio_actual = Path(__file__).resolve().parent


def agregar_usuario(login, empresas, roles, activo=True):
    """Agrega un usuario con una lista de roles."""

    coleccion_usuarios = database.Usuarios

    usuario = {
        "nombre": login,
        "apellido": login,
        "empresas": empresas,
        "login": login,
        "clave": "!2E",
        "roles": roles,
        "activo": activo
    }

    existente = coleccion_usuarios.find_one({"login": login})

    if existente:
        coleccion_usuarios.update_one(
            {"_id": existente["_id"]},
            {"$set": usuario}
        )

        duplicados = coleccion_usuarios.find(
            {"login": login, "_id": {"$ne": existente["_id"]}},
            {"_id": 1}
        )
        ids_duplicados = [documento["_id"] for documento in duplicados]

        if ids_duplicados:
            coleccion_usuarios.delete_many({"_id": {"$in": ids_duplicados}})
            print(f"Usuario '{login}' actualizado. Duplicados eliminados: {len(ids_duplicados)}")
        else:
            print(f"Usuario '{login}' actualizado correctamente.")

        return

    coleccion_usuarios.insert_one(usuario)
    print(f"Usuario '{login}' agregado correctamente.")


def agregar_rol(rol, descripcion):
    """Agrega un rol."""

    coleccion_roles = database.Roles

    nuevo_rol = {
        "rol": rol,
        "descripcion": descripcion,
        "activo": True
    }

    existente = coleccion_roles.find_one({"rol": rol})

    if existente:
        coleccion_roles.update_one(
            {"_id": existente["_id"]},
            {"$set": nuevo_rol}
        )

        duplicados = coleccion_roles.find(
            {"rol": rol, "_id": {"$ne": existente["_id"]}},
            {"_id": 1}
        )
        ids_duplicados = [documento["_id"] for documento in duplicados]

        if ids_duplicados:
            coleccion_roles.delete_many({"_id": {"$in": ids_duplicados}})
            print(f"Rol '{rol}' actualizado. Duplicados eliminados: {len(ids_duplicados)}")
        else:
            print(f"Rol '{rol}' actualizado correctamente.")

        return

    coleccion_roles.insert_one(nuevo_rol)
    print(f"Rol '{rol}' agregado correctamente.")


def rutas():

    coleccion_rutas = database.Rutas

    rutas_json = directorio_actual / "rutas.json"

    print(f"Importando Rutas desde: {rutas_json}")

    with open(rutas_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    if not datos:
        print("El archivo está vacío")
        return

    creadas = 0
    actualizadas = 0
    duplicadas_eliminadas = 0

    for ruta in datos:
        filtro = {
            "rol": ruta.get("rol"),
            "path": ruta.get("path")
        }
        existente = coleccion_rutas.find_one(filtro)

        if existente:
            coleccion_rutas.update_one(
                {"_id": existente["_id"]},
                {"$set": ruta}
            )
            actualizadas += 1

            duplicados = coleccion_rutas.find(
                {**filtro, "_id": {"$ne": existente["_id"]}},
                {"_id": 1}
            )
            ids_duplicados = [documento["_id"] for documento in duplicados]

            if ids_duplicados:
                coleccion_rutas.delete_many({"_id": {"$in": ids_duplicados}})
                duplicadas_eliminadas += len(ids_duplicados)

            continue

        coleccion_rutas.insert_one(ruta)
        creadas += 1

    print(
        f"Rutas procesadas. Creadas: {creadas}. "
        f"Actualizadas: {actualizadas}. "
        f"Duplicadas eliminadas: {duplicadas_eliminadas}."
    )


# ------------------------------------------------------------

rutas()

agregar_usuario(
    "admin",
    ["Techiar"],
    ["Administrador"],
    True
)

agregar_rol(
    "Administrador",
    "Administrador"
)
