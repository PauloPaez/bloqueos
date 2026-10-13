def rolesSh(item):
    return {
        "id": str(item.get("_id")),
        "rol": item.get("rol"),
        "descripcion": item.get("descripcion"),
        "activo": item.get("activo"),
    }
