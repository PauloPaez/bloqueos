#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # Sin color


find . -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} \;

echo -e "${RED}Este framework crea la estructura de directorios y archivos para el proyecto${NC}"
echo "------------------------------------------------------------------------------------------"
read -p "Ingrese Nombre de Base de Datos:: " DB
echo "---------------------------------BACKEND--------------------------------------------------"

./estructura/crearBack.sh
python3 ./templates/crearEngine.py ${DB} > ../back/scripts/conf/engine.py

# #  ----------------------------------------------------

./estructura/crearFront.sh
mv front ..
 
mkdir -p ../front/src/{store,components}

cp ./templates/apiSlice.jsx ../front/src/store
cp ./templates/appSlice.jsx ../front/src/store
cp ./templates/store.jsx ../front/src/store
cp ./templates/App.jsx ../front/src
cp ./templates/cargando.gif ../front/src/assets
cp ./templates/spiral.gif ../front/src/assets
cp ./templates/TDS.* ../front/src/assets
cp ./templates/index.html ../front
cp ./templates/index.css ../front/src
cp -r ./templates/common ../front/src
cp -r ./templates/administracion ../front/src/components
cp -r ./templates/Personas ../front/src/components
cp -r ./templates/hooks ../front/src
cp -r ./templates/layout ../front/src
cp -r ./templates/config ../front/src
cp ./templates/.env.development ../front
cp ./templates/.env.production ../front

# echo "---------------------------------USUARIOS, ROLES Y RUTAS----------------------------------"

source  ../venv/bin/activate && python3 ./estructura/crearUsuarios-Roles-Rutas.py ${DB} && deactivate

# ---------------------------------------------------------------------------------------
echo -e "${RED}Termino la herramienta de estructura...${NC}"
