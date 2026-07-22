RED='\033[0;31m'
NC='\033[0m' # Sin color
CYAN='\033[0;36m'
echo -e "${CYAN}${BOLD}Este framework crear un Select en el Modelo${NC}"

read -p "nombre modelo : " modelo
if [[ -z "$modelo" ]]; then
  echo -e "${RED}Error: No se ingresó el nombre del modelo. Saliendo...${NC}"
  exit 1
fi

# Verificar si el archivo existe
archivo="./agregarModeloFuentes/diccModelo/${modelo}.json"
echo $archivo
if [[ ! -f "$archivo" ]]; then
  echo -e "${BLINK}${RED}Error: El archivo ${archivo} no existe. Saliendo...${NC}"
  exit 1
fi

echo -e "${CYAN}Creando el modelo ${modelo}...${NC}"

python3 ./agregarSelect/agregarSelect.py  ${modelo}


# ----------------------------------------------------

echo -e "${RED}Termino las herramientas de crear el Select ${modelo}...${NC}"

