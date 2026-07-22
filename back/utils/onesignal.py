import os
import requests
from dotenv import load_dotenv

load_dotenv()

ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY")


def enviar_notificacion(player_id: str, titulo: str, mensaje: str, data: dict):
    url = "https://onesignal.com/api/v1/notifications"

    print("✅ APP ID:", ONESIGNAL_APP_ID)
    print("✅ API KEY:", ONESIGNAL_API_KEY)
    print("✅ SUBSCRIPTION ID:", player_id)

    payload = {
        "app_id": ONESIGNAL_APP_ID,

        # ✅ CLAVE PARA ONESIGNAL v5
        "include_subscription_ids": [player_id],

        # ✅ OBLIGATORIO: INGLÉS
        "headings": {
            "en": titulo,
            "es": titulo
        },
        "contents": {
            "en": mensaje,
            "es": mensaje
        },
        "data": data or {}
    }

    headers = {
        "Authorization": f"Basic {ONESIGNAL_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("✅ STATUS:", response.status_code)
    print("✅ RESPONSE:", response.text)

    return response.json()
