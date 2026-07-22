def usuariosSh(item):
    return {
        "id": str(item.get("_id")),
        "nombre": item.get("nombre"),
        "apellido": item.get("apellido"),
        "empresas": item.get("empresas"),        
        "login": item.get("login"),
        "clave": item.get("clave"),
        "roles": item.get("roles"),
        "activo": item.get("activo"),
    }
