RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color
CYAN='\033[0;36m'
BOLD='\033[1m' # Negrita
BLINK='\033[5m' # Parpadeante

# Combinar códigos para texto rojo, negrita y parpadeante
RED_BOLD_BLINK="${RED}${BOLD}${BLINK}"
BLUE_BOLD_BLINK="${BLUE}${BOLD}${BLINK}"

clear

echo -e "${CYAN}-----------------------------------------${NC}"
read -p "$(echo -e Ingrese Nombre de ${RED_BOLD_BLINK}Base de Datos${NC}: )" DB
echo -e "${RED}-----------------------------------------${NC}"
read -p "$(echo -e Ingrese Nombre de ${BLUE_BOLD_BLINK}Modelo${NC}: )" modelo
echo -e "${CYAN}-----------------------------------------${NC}"

# python3 agregarComponentFuentes/agregarEnArchivoRoutes.py ${modelo}

# ----------------------------------------------------

source  ../venv/bin/activate && python3 ./agregarRutas.py ${modelo} ${DB} && deactivate
