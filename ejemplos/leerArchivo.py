import json
from pathlib import Path

CAMPOS = [(0,10,'padron'), (10,30,'nombre'), (30,40,'fecha'), (40,48,'sueldo'), (48,51,'pais')]
registros = []

with open(Path('dirA/titulares.txt'), 'r', encoding='utf-8') as f:
    for linea in f:
        linea = linea.rstrip('\n\r')
        registro = {
            'padron': int(linea[0:10].strip() or 0),
            'nombre': linea[10:30].strip(),
            'fecha': linea[30:40].strip(),
            'sueldo': float(linea[40:48].strip() or 0.0),
            'pais': linea[48:51].strip()
        }
        registros.append(registro)

with open('titulares.json', 'w', encoding='utf-8') as f:
    json.dump(registros, f, ensure_ascii=False, indent=2)

print(f"✅ {len(registros)} registros guardados en titulares.json")
