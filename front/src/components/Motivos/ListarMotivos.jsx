import React, { useState, useEffect, useCallback } from "react";
import { usePostMotivosByFieldMutation } from "../../store/apiSlice";
import { useDispatch, useSelector } from "react-redux";
import { setModuloState, resetModulo, setFiltroListado } from "../../store/appSlice";
import FiltroMotivos from "./FiltroMotivos";
import { convertirMesANumero } from "../../common/meses"; 
import { WS_BASE_URL } from "../../config/api";
import '../../common/tables.css';
import { formularioCampos } from './FormularioListar';
const ListarMotivos = () => {
  const dispatch = useDispatch();
  const filtroListado = useSelector((state) => state.listado.filtro);
  const [postMotivos] = usePostMotivosByFieldMutation();
  const [datos, setDatos] = useState([]);
  const user = useSelector((state) => state.acceso.user);
  const [isLoading, setIsLoading] = useState(true);
  // Definir el filtro inicial
  const [mostrarFiltroInicial, setMostrarFiltroInicial] = useState(false);
  const filtroInicial = { "activo": true };
  const postFijo = { "empresa": user.empresa };
  // Cargar datos iniciales
  useEffect(() => {
    const cargarDatosIniciales = async () => {
      setIsLoading(true);
      try {
        const filtroActual = { ...filtroInicial, ...postFijo };
        console.log("Cargando datos con filtro:", filtroActual);
        dispatch(setFiltroListado(filtroActual));
        const result = await postMotivos(filtroActual).unwrap();
        setDatos(result || []);
        setMostrarFiltroInicial(result?.length === 0);
      } catch (err) {
        console.error("Error fetching datos iniciales:", err);
        setDatos([]);
        setMostrarFiltroInicial(true);
      } finally {
        setIsLoading(false);
      }
    };
    cargarDatosIniciales();
  }, []); // Solo se ejecuta una vez al montar
  // Manejar cambios en los filtros (cuando el usuario aplica nuevos filtros)
  useEffect(() => {
    if (filtroListado && Object.keys(filtroListado).length > 0) {
      const aplicarFiltro = async () => {
        setIsLoading(true);
        dispatch(resetModulo({ modulo: 'empleado' }));
        const filtroTransformado = { ...filtroListado };
        if (filtroTransformado.mes && typeof filtroTransformado.mes === "string") {
          const numeroMes = convertirMesANumero(filtroTransformado.mes);
          if (numeroMes) {
            filtroTransformado.mes = numeroMes;
          }
        }
        try {
          const result = await postMotivos(filtroTransformado).unwrap();
          setDatos(result || []);
          setMostrarFiltroInicial(result?.length === 0);
        } catch (err) {
          console.error("Error fetching datos con filtro:", err);
          setDatos([]);
          setMostrarFiltroInicial(true);
        } finally {
          setIsLoading(false);
        }
      };
      aplicarFiltro();
    }
  }, [filtroListado, dispatch, postMotivos]);
  const refetch = useCallback(() => {
    if (filtroListado && Object.keys(filtroListado).length > 0) {
      return postMotivos(filtroListado).unwrap()
        .then(result => setDatos(result || []))
        .catch(err => console.error("Error recargando datos:", err));
    }
    return Promise.resolve();
  }, [filtroListado, postMotivos]);
  // WebSocket
  useEffect(() => {
    const websocket = new WebSocket(`${WS_BASE_URL}ws/motivos`);
    websocket.onmessage = (event) => {
      console.log("Notificación recibida:", event.data);
      refetch();
    };
    websocket.onclose = () => {
      console.log("WebSocket cerrado");
    };
    return () => {
      websocket.close();
    };
  }, [refetch]);
   const handleRowClick = (dato) => {
    dispatch(setModuloState({
      modulo: 'motivos',
      nuevosDatos: {
        datos: dato,
        estadoEdicion: true
      }
    }));
  };
  const handleResetFilter = () => {
    const filtroReset = { ...filtroInicial, ...postFijo };
    dispatch(setFiltroListado(filtroReset));
    postMotivos(filtroReset).unwrap()
      .then(result => {
        setDatos(result || []);
        setMostrarFiltroInicial(result?.length === 0);
      })
      .catch(err => console.error("Error recargando datos reset:", err));
  };
  if (isLoading) {
    return (
      <div className="text-center my-4">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
        <p className="mt-2">Cargando motivos...</p>
      </div>
    );
  }
  // Filtrar campos visibles
  const camposVisibles = formularioCampos.filter(field => field.placeholder !== "no_visible");
  return (
    <div>
      <FiltroMotivos filtroInicial={filtroInicial} postFijo={postFijo} />
      {mostrarFiltroInicial && (
        <div className="alert alert-info">
          No hay datos disponibles con los filtros actuales.
          <button onClick={handleResetFilter} className="btn btn-link">
            Mostrar todos los datos
          </button>
        </div>
      )}
      {datos.length > 0 ? (
        <div className="table-container-wrapper">
          <div className="table-container">
            <table className="sticky-table">
              <thead>
                <tr className="sticky-header">
                  {camposVisibles.map((field) => (
                    <th key={field.name}>{field.label}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {datos.map((item, index) => (
                  <tr key={index} onClick={() => handleRowClick(item)}>
                    {camposVisibles.map((field) => {
                      const valor = item[field.name];
                      if (field.type === "date" && valor) {
                        return <td key={field.name}>{new Date(valor).toLocaleDateString('es-ES')}</td>;
                      }
                      if (typeof valor === "boolean") {
                        return <td key={field.name}>{valor ? "SI" : "NO"}</td>;
                      }
                      if (field.name === "nota") {
                        return <td key={field.name}>{valor && valor.trim() !== "" ? "SI" : "NO"}</td>;
                      }
                      return <td key={field.name}>{valor || "-"}</td>;
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        !mostrarFiltroInicial && <p>No hay datos disponibles</p>
      )}
    </div>
  );
};
export default ListarMotivos;
