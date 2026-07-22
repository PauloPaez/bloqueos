RED='\033[0;31m'
NC='\033[0m' # Sin color
CYAN='\033[0;36m'
echo -e "${CYAN}${BOLD}Este framework crear un modelo y los scripts correspondientes${NC}"

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

python3 ./agregarModeloFuentes/agregarModelo.py  ${modelo}
python3 ./agregarModeloFuentes/agregarSchema.py ${modelo}
python3 ./agregarModeloFuentes/agregarQuery.py ${modelo}
python3 ./agregarModeloFuentes/agregarRouter.py ${modelo}
python3 ./agregarModeloFuentes/modificarMain.py ${modelo}
python3 ./agregarModeloFuentes/modificarApiSlice.py ${modelo}
python3 ./agregarModeloFuentes/modificarWebSocket.py ${modelo}

#--------------------FRONT--------------------------

python3 agregarComponentFuentes/componenteListar.py ${modelo}
python3 agregarComponentFuentes/componenteEditar.py ${modelo}
python3 agregarComponentFuentes/agregarStateModulo.py ${modelo}
python3 agregarComponentFuentes/generarFiltro.py ${modelo}
python3 agregarComponentFuentes/componenteActualizar.py ${modelo}
python3 agregarComponentFuentes/agregarEnArchivoRoutes.py ${modelo}

python3 agregarSelect/agregarSelect.py ${modelo}

#copiar archivos estaticos desde templates al nuevo componente
capitalizado="${modelo^}"
echo modelo: $capitalizado

cp agregarComponentFuentes/templates/camposRequeridosFormulario.js ../front/src/components/${capitalizado}/
cp agregarComponentFuentes/templates/camposValidacion.js ../front/src/components/${capitalizado}/
cp agregarComponentFuentes/templates/formularioSeparadores.js ../front/src/components/${capitalizado}/

# ----------------------------------------------------
# read -p "Ingrese Nombre de Base de Datos:: " DB
source  ../venv/bin/activate && python3 ./agregarRutas.py ${modelo} && deactivate
# ---------------------------------------------------------------------------------------

echo -e "${RED}Termino las herramientas de crear a ${modelo}...${NC}"

