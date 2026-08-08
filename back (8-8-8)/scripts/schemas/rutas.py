def rutasSh(item):
    return {
        "id": str(item.get("_id")),
        "rol": item.get("rol"),
        "componente": item.get("componente"),
        "path": item.get("path"),
        "app": item.get("app", False)
    }
