def motivosSh(item):
    return {
        "id": str(item.get("_id")),
        "motivo": item.get("motivo"),
        "lleva_fecha": item.get("lleva_fecha", False),
        "login": item.get("login"),
        "empresa": item.get("empresa"),
        "activo": item.get("activo"),
    }
