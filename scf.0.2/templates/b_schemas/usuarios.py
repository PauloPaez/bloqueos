def usuariosSh(item):
    return {
        "id": str(item.get("_id")),
        "nombre": item.get("nombre"),
        "apellido": item.get("apellido"),
        "empresas": item.get("empresas"),  
        "dni": item.get("dni"),
        "calle_nro": item.get("calle_nro"),
        "barrio": item.get("barrio"),
        "departamento": item.get("departamento"),
        "provincia": item.get("provincia"),
        "cargo": item.get("cargo"),     
        "login": item.get("login"),
        "clave": item.get("clave"),
        "roles": item.get("roles"),
        "activo": item.get("activo"),
    }
