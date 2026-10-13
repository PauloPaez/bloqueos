from pathlib import Path
import sys
import re
#from pymongo import MongoClient

# ---- Configuración de paths ----
ruta_conf_motor = Path(__file__).resolve().parent.parent / 'back' / 'scripts' / 'conf'
sys.path.append(str(ruta_conf_motor))

import engine  # importa engine.py directamente

# ---- Base de datos ----
nombre_base = engine.database.name
print('Base de datos por defecto:', nombre_base)

