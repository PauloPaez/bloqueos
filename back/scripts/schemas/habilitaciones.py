def habilitacionesSh(item):
    return {
        "id": str(item.get("_id")),
        "rol": item.get("rol"),
        "periodo": item.get("periodo"),
        "fecha_cierre": item.get("fecha_cierre"),
        "cerrado": item.get("cerrado", False),
        "login": item.get("login"),
        "empresa": item.get("empresa"),
        "activo": item.get("activo"),
    }
