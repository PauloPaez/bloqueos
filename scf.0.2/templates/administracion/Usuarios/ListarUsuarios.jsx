// ListarUsuarios.jsx
import React, { useState, useEffect } from "react";
import { useGetUsuariosQuery } from "../../../store/apiSlice";
import { useDispatch } from "react-redux";
import { setFila } from "../../../store/appSlice";
const ListarUsuarios = () => {
  const dispatch = useDispatch();
  const { data: datos, error, isLoading, refetch } = useGetUsuariosQuery();
  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8000/ws/usuarios");
    websocket.onmessage = (event) => {
      console.log("Notificación recibida:", event.data);
      refetch(); // Refetch los datos cuando llega una notificación
    };
    websocket.onclose = () => {
      console.log("WebSocket cerrado");
    };
    return () => {
      websocket.close();
    };
  }, [refetch]);
  if (isLoading) return <p>Cargando Usuarios...</p>;
  if (error) return <p>Error al cargar Usuarios: {error.message}</p>;
  if (!datos || datos.length === 0) return <p>No hay datos disponibles</p>;
    const formFields = [
	{name: "nombre", label: "Nombre", placeholder: "Nombre del usuario", type: "text"},
	{name: "apellido", label: "Apellido", placeholder: "Apellido del usuario", type: "text"},
	{name: "empresas", label: "Empresas", placeholder: "Empresa donde trabaja", type: "text"},  
	{name: "login", label: "Login", placeholder: "Ingrese Login", type: "text"},
	{name: "clave", label: "Clave", placeholder: "****", type: "text"},
	{name: "roles", label: "Roles", placeholder: "Lista de Roles", type: "text"},
	{name: "activo", label: "Activo", placeholder: "Activo", type: "checkbox"},
  ];
   const columnas = Object.keys(datos[0]).filter((key) => {
    // Filtrar columnas basadas en formFields excluyendo campos con placeholder "no_visible"
    const field = formFields.find((f) => f.name === key);
    return field && field.placeholder !== "no_visible";
  });
  // Función para manejar la selección de una fila
  const handleRowClick = (socio) => {
    dispatch(setFila(socio)); // Despacha la acción para guardar el socio seleccionado
    console.log("Fila seleccionada:", socio);
  };
  return (
    <div>
      <table className="table table-striped">
        <thead>
          <tr>
            {columnas.map((columna) => (
              <th key={columna}>{columna}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {datos.map((item, index) => (
            <tr key={index} onClick={() => handleRowClick(item)}>
              {columnas.map((columna) => (
                <td key={columna}>
                  {Array.isArray(item[columna]) ? item[columna].join(", ") 
                    : typeof item[columna] === "boolean" 
                    ? item[columna]
                      ? "SI"
                      : "NO"
                    : item[columna]} {/* Si no, muestra el valor directamente */}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default ListarUsuarios;
