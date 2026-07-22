def personasSh(item):
    return {
        "id": str(item.get("_id")),
        "dni": item.get("dni"),
        "nombre": item.get("nombre"),
        "apellido": item.get("apellido"),
        "empresa_cnx": item.get("empresa_cnx"),
        "login_cnx": item.get("login_cnx"),
        "calle_nro": item.get("calle_nro"),
        "barrio": item.get("barrio"),
        "departamento": item.get("departamento"),
        "provincia": item.get("provincia"),
        "cargo": item.get("cargo"),
        "login": item.get("login"),
        "empresa": item.get("empresa"),
        "activo": item.get("activo"),
    }
