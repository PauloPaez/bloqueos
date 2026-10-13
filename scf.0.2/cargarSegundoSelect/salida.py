Criterio: const dispatch = useDispatch();
Pre: False
Código Nuevo:  const { data: Categorias = [] } = useGetDistinctTipo_notasQuery('categoria');

---

Criterio: const filaSeleccionada = useSelector((state) => state.modulos.nro_notas).datos;
Pre: False
Código Nuevo:     const [Tipos, setTipos] = useState([]);
   const [recuperarTipos] = usePostTipo_notasByFieldMutation(); 

  const datosSelect = {
    "categorias": Categorias,
    "tipos": Tipos,
  };

---

Criterio:   const onSubmit = async (data) => {
Pre: True
Código Nuevo:   
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
    }, [categoriaSeleccionado, cargarTipos]);

---

