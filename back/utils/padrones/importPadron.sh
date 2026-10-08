#!/usr/bin/env bash
set -euo pipefail

# Raíz del proyecto: back/utils/padrones -> 3 niveles arriba
DIR_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="$(cd "$DIR_SCRIPT/../../.." && pwd)"
ARCHIVO_ENV="$RAIZ/.env"

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

mongoimport \
  --host localhost \
  --port 27100 \
  --username bloqueos_test \
  --password "$PASSWORD_DB" \
  --authenticationDatabase "$MONGO_DB" \
  --db "$MONGO_DB" \
  --collection Escuelas \
  --file "$ARCHIVO_JSON" \
  --jsonArray \
  --drop
