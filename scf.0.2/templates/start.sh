#!/bin/bash

# Ruta al entorno virtual
VENV_PATH=".venv/bin/activate"

# Verifica si el archivo de activación del entorno virtual existe
if [ ! -f "$VENV_PATH" ]; then
    echo "Error: No se encontró el entorno virtual en $VENV_PATH"
    exit 1
fi

# Activa el entorno virtual
source "$VENV_PATH"

# Comando para arrancar Uvicorn
UVICORN_COMMAND="uvicorn main:app --reload"

echo "Iniciando Uvicorn..."
$UVICORN_COMMAND

