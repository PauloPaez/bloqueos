RED='\033[0;31m'
NC='\033[0m' # Sin color
CYAN='\033[0;36m'
echo -e "${CYAN}${BOLD}Insertar un select a cun componente EDITAR ${NC}"

read -p "Modulo Destino : " componente_a_modificar
if [[ -z "$componente_a_modificar" ]]; then
  echo -e "${RED}Error: No se ingresó el nombre del modelo destino. Saliendo...${NC}"
  exit 1
fi

read -p "Modulo Origen : " Modelo_del_select
if [[ -z "$Modelo_del_select" ]]; then
  echo -e "${RED}Error: No se ingresó el nombre del modelo origen. Saliendo...${NC}"
  exit 1
fi

read -p "Campo Opcion del Select : " labelKey
if [[ -z "$labelKey" ]]; then
  echo -e "${RED}Error: No se ingresó el nombre del campo. Saliendo...${NC}"
  exit 1
fi

read -p "Campo del Formulario de componente Destino : " campo_del_formulario
if [[ -z "$campo_del_formulario" ]]; then
  echo -e "${RED}Error: No se ingresó el campo del formulario. Saliendo...${NC}"
  exit 1
fi

read -p "Label del campo en el Formulario de componente Destino : " Label
if [[ -z "$Label" ]]; then
  echo -e "${RED}Error: No se ingresó el campo del formulario. Saliendo...${NC}"
  exit 1
fi  
if [[ -z "$campo_del_formulario" ]]; then
  echo -e "${RED}Error: No se ingresó el campo del formulario. Saliendo...${NC}"
  exit 1
fi

echo -e "${CYAN}Creando el modelo ${modelo}...${NC}"
# ----------------------------------------------------

python3 ./agregarSelect/agregarSelectEnComponente.py ${componente_a_modificar} ${Modelo_del_select} ${labelKey} ${campo_del_formulario} ${Label}
# ----------------------------------------------------

echo -e "${RED}Termino las herramientas para asignar un Select ${componente_a_modificar}...${NC}"

