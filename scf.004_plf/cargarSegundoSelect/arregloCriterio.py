arregloCodigo = [{
    'criterio': 'const dispatch = useDispatch();',
    'pre': False, 
    'codigoNuevo': " const { data: Categorias = [] } = useGetDistinctTipo_notasQuery('categoria');",
},
{
    'criterio': 'const filaSeleccionada = useSelector((state) => state.modulos.nro_notas).datos;',
    'pre': False,
    'codigoNuevo': """    const [Tipos, setTipos] = useState([]);
   const [recuperarTipos] = usePostTipo_notasByFieldMutation(); 

  const datosSelect = {
    "categorias": Categorias,
    "tipos": Tipos,
  };"""  
},
{
    'criterio': '  const onSubmit = async (data) => {',
    'pre': True,
    'codigoNuevo': """  
    const categoriaSeleccionado = watch('nro_notas.0.categoria')
      // Función para cargar los tomos
    const cargarTipos = useCallback(async (categoria) => {
        if (!categoria) {
           setTipos([]);
            return;
        }
        try {
            const result = await recuperarTipos({ categoria }).unwrap();
            // Asumiendo que result es un array de objetos con propiedad tipo
            const TiposUnicos = [...new Set(
                result
                    .filter(item => item.tipo)
                    .map(item => item.tipo.toString().trim())
            )];
            setTipos(TiposUnicos);
        } catch (error) {
            console.error("Error al cargar Tipos:", error);
            setTipos([]);
        }
    }, [recuperarTipos]);
    
    // Efecto que se dispara cuando cambia el libro seleccionado
    useEffect(() => {
        console.log(categoriaSeleccionado)
        cargarTipos(categoriaSeleccionado);
    }, [categoriaSeleccionado, cargarTipos]);"""
}]

for codigo in arregloCodigo:
    print("Criterio:", codigo.get('criterio', codigo.get('criterio', 'No especificado')))
    print("Pre:", codigo['pre'])
    print("Código Nuevo:", codigo['codigoNuevo'])
    print("\n---\n")
