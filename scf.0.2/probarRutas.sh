read -p "Ingrese Nombre de Mdelo:: " model
read -p "Ingrese Nombre de Base de Datos:: " DB
source  /home/paulo/Documentos/aplicaciones/python_app/'login y componetes'/venv/bin/activate && python3 ./agregarRutas.py ${model} ${DB} && deactivate
