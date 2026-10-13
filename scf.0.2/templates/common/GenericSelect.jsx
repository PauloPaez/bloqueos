import React, { useState, useEffect } from "react";

const GenericSelect = ({
  value,
  onSelect,
  useQuery,
  valueKey,
  labelKey,
  placeholder,
  label,
  multiple
}) => {

  const [postQuery] = useQuery();


  const [data, setData] = useState([]); // Agrega este estado
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);


const fetchData = async () => {
  try {
    setIsLoading(true);
    const result = await postQuery({ "activo": true }).unwrap();
    setData(result); // Actualiza el estado con los datos
    setError(null);
  } catch (err) {
    console.error("Error fetching datos:", err);
    setError(err);
    setData([]);
  } finally {
    setIsLoading(false);
  }
};
  useEffect(() => {
    fetchData();
  }, []);

  if (isLoading) return <p>Cargando...</p>;
  if (error) return <p>Error al cargar datos: {error.message}</p>;
  if (!data || data.length === 0) return <p>No hay datos disponibles</p>;

  return (
    <div className="mb-3">
      <select
        id="select"
        value={value || (multiple ? [] : "")} // Manejar múltiples valores
        onChange={(e) => {
          if (multiple) {
            // Si es múltiple, obtener todos los valores seleccionados
            const selectedOptions = Array.from(e.target.selectedOptions).map(
              (option) => option.value
            );
            onSelect(selectedOptions);
          } else {
            // Si no es múltiple, obtener el valor único
            onSelect(e.target.value);
          }
        }}
        className="form-control"
        multiple={multiple} // Habilitar selección múltiple o no
      >
        <option value="">{placeholder}</option>
        {data.map((item) => (
          <option key={item[valueKey]} value={item[valueKey]}>
            {item[labelKey]}
          </option>
        ))}
      </select>
    </div>
  );
};

export default GenericSelect;