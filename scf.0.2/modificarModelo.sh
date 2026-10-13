RED='\033[0;31m'
NC='\033[0m' # Sin color
CYAN='\033[0;36m'
echo -e "${CYAN}${BOLD}Este framework modificará el modelo y el esquema ${NC}"

read -p "nombre modelo : " modelo
if [[ -z "$modelo" ]]; then
  echo -e "${RED}Error: No se ingresó el nombre del modelo. Saliendo...${NC}"
  exit 1
fi

echo -e "${CYAN}Creando el modelo ${modelo}...${NC}"

python3 ./agregarModeloFuentes/agregarModelo.py  ${modelo}
python3 ./agregarModeloFuentes/agregarSchema.py ${modelo}


echo -e "${RED}Termino las herramientas de crear a ${modelo}...${NC}"