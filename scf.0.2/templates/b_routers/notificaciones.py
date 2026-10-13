from fastapi import APIRouter
from utils.onesignal import enviar_notificacion
from scripts.models.usuarios import Usuarios
notificaciones = APIRouter()


@notificaciones.post("/test-notificacion")
def test_notificacion():
    player_id = "814c96b1-54c6-44a6-bc78-f951af557ddd"

    respuesta = enviar_notificacion(
        player_id=player_id,
        titulo="🔔 Prueba subastAR",
        mensaje="Llego un nuevo PEDIDO 🚀",
        data={"screen": "Home"}
    )

    return respuesta


@notificaciones.post("/notificacion_grupo")
def notificacion_a_grupo(players: list, mensaje: str = "subastAR tiene Noticias"):
    for player in players:
        player_pushID = player['pushID'] 
        print("Player pushID:", player_pushID)
        respuesta = enviar_notificacion(
            player_id = player_pushID,
            titulo="🔔 Notificación de subastAR",
            mensaje=mensaje,
            data={"screen": "Home"}
    )
    print("Respuesta de OneSignal:", respuesta)
    return respuesta
