#!/usr/bin/env bash
set -euo pipefail

# Raíz del proyecto: back/utils/padrones -> 3 niveles arriba
DIR_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="$(cd "$DIR_SCRIPT/../../.." && pwd)"
ARCHIVO_ENV="$RAIZ/back/.env"

echo "Directorio raíz del proyecto: $RAIZ"

if [[ ! -f "$ARCHIVO_ENV" ]]; then
  echo "Error: no se encontró $ARCHIVO_ENV" >&2
  exit 1
fi

# Cargar variables del .env
set -a
source "$ARCHIVO_ENV"
set +a

# Validar variables necesarias
: "${MONGO_DB:?Falta MONGO_DB en el .env}"
: "${PASSWORD_DB:?Falta PASSWORD_DB en el .env}"

# Archivo a importar (parámetro opcional)
ARCHIVO_JSON="${1:-SETIEMBRE26.json}"
ARCHIVO_JSON_PATH="$RAIZ/datos/fuentes_formateadas/$ARCHIVO_JSON"
echo "Importando archivo $ARCHIVO_JSON a la base de datos $MONGO_DB..."
echo "Usando usuario: bloqueos_test y contraseña: $PASSWORD_DB"
echo "Conexión a la base de datos en: $IP_DB:27100"
echo "Archivo JSON: $ARCHIVO_JSON_PATH"
mongoimport \
  --host "$IP_DB" \
  --port 27100 \
  --username bloqueos_test \
  --password "$PASSWORD_DB" \
  --authenticationDatabase "$MONGO_DB" \
  --db "$MONGO_DB" \
  --collection Escuelas \
  --file "$ARCHIVO_JSON_PATH" \
  --jsonArray \
  --drop
