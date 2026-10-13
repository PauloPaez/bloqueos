 
  const recuperarProvincia = useCallback(async (pais) => {
    if (!pais) return []; // Mejor retornar array vacío para consistencia
    
    const filtro = { pais };
    
    try {
      const result = await buscarProvincia(filtro).unwrap();
      const provinciasDistinct = [...new Set(
        result
          .filter(item => item.provincia) // Asegura que provincia no sea null/undefined
          .map(item => item.provincia.trim()) // Limpia espacios
      )];
      
      return provinciasDistinct;
