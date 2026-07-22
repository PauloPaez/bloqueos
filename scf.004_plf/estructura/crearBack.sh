#!/bin/bash

# Crear la estructura de directorios
mkdir -p ../back/scripts/{querys,models,schemas,routers,conf}
mkdir -p ../back/utils
mkdir -p ../back/run 
mkdir -p ../back/logs

# Crear el archivo main.py con el contenido deseado

cp ./templates/main.py ../back/main.py
cp ./templates/start.sh ../back
cp ./templates/b_models/* ../back/scripts/models
cp ./templates/b_querys/* ../back/scripts/querys
cp ./templates/b_routers/* ../back/scripts/routers
cp ./templates/b_schemas/* ../back/scripts/schemas
cp ./templates/utils/* ../back/utils
# Crear un entorno virtual

python3 -m venv ../back/.venv

# Activar el entorno virtual

source ../back/.venv/bin/activate

# Instalar los paquetes necesarios

pip install fastapi motor uvicorn[standard] python-multipart openpyxl pandas requests
deactivate

#Crear entorno virtual para insertar rutas

python3 -m venv ../venv
source ../venv/bin/activate
pip install pymongo motor
deactivate

# echo "Entorno virtual activado, paquetes instalados y main.py creado con contenido."

