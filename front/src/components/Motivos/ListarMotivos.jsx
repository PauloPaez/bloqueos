import React, { useState, useEffect, useCallback } from "react";
import { usePostMotivosByFieldMutation } from "../../store/apiSlice";
import { useDispatch, useSelector } from "react-redux";
import {
  setModuloState,
  resetModulo,
} from "../../store/appSlice";
import useFiltroListado from "../../hooks/useFiltroListado";
import FiltroMotivos from "./FiltroMotivos";
import { convertirMesANumero } from "../../common/meses"; 
import { WS_BASE_URL } from "../../config/api";
import '../../common/tables.css';
import './ListarMotivos.css';
import { formularioCampos } from './FormularioListar';
import { Pencil, Plus, SearchX, Tags } from "lucide-react";

// editable: solo en la pantalla Actualizar, donde existe el modal de edición.
const ListarMotivos = ({ claveFiltro = "motivos:listar", editable = false }) => {
  const dispatch = useDispatch();
  const {
    filtro: filtroListado,
    filtroGuardado,
    guardarFiltro,
    resetearFiltro,
  } = useFiltroListado(claveFiltro, { limpiarAlDesmontar: true });
  const [postMotivos] = usePostMotivosByFieldMutation();
  const [datos, setDatos] = useState([]);
  const user = useSelector((state) => state.acceso.user);
  const [isLoading, setIsLoading] = useState(true);
  // Definir el filtro inicial
  const [mostrarFiltroInicial, setMostrarFiltroInicial] = useState(false);
  // Sin filtro inicial: se listan activos e inactivos, así "Activo: Todos" funciona.
  const filtroInicial = {};
  const postFijo = { "empresa": user.empresa };
  // Cargar datos iniciales
  useEffect(() => {
    const cargarDatosIniciales = async () => {
      setIsLoading(true);
      try {
        const filtroActual = filtroGuardado ?? { ...filtroInicial, ...postFijo };
        console.log("Cargando datos con filtro:", filtroActual);
        guardarFiltro(filtroActual);
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
    if (!editable) return;
    dispatch(setModuloState({
      modulo: 'motivos',
      nuevosDatos: {
        datos: dato,
        estadoEdicion: true,
        mostrarModal: true,
      }
    }));
  };
  const handleAgregar = () => {
    dispatch(setModuloState({
      modulo: 'motivos',
      nuevosDatos: {
        datos: null,
        estadoEdicion: false,
        mostrarModal: true,
      }
    }));
  };
  const handleResetFilter = () => {
    const filtroReset = { ...filtroInicial, ...postFijo };
    resetearFiltro(filtroReset);
    postMotivos(filtroReset).unwrap()
      .then(result => {
        setDatos(result || []);
        setMostrarFiltroInicial(result?.length === 0);
      })
      .catch(err => console.error("Error recargando datos reset:", err));
  };
  // Hay filtros del usuario si el filtro tiene algo más que lo fijo (empresa).
  const hayFiltros = Object.keys(filtroListado).some((clave) => !(clave in postFijo));
  // Filtrar campos visibles
  const camposVisibles = formularioCampos.filter(field => field.placeholder !== "no_visible");
  const cantidadColumnas = camposVisibles.length + (editable ? 1 : 0);
  return (
    <div>
      <header className="listado-header">
        <h1 className="listado-titulo">Listado de Motivos</h1>
        {editable && (
          <button type="button" className="btn btn-dark motivos-agregar" onClick={handleAgregar}>
            <Plus size={16} aria-hidden="true" />
            Agregar motivo
          </button>
        )}
      </header>
      <div className="motivos-filtro">
        <FiltroMotivos
          filtroInicial={filtroInicial}
          postFijo={postFijo}
          claveFiltro={claveFiltro}
        />
      </div>
      {isLoading ? (
        <div className="text-center my-4" role="status" aria-live="polite">
          <div className="spinner-border text-primary" aria-hidden="true" />
          <p className="mt-2">Cargando motivos...</p>
        </div>
      ) : (
        <div className="table-container-wrapper">
          <div className="table-container">
            <table className="sticky-table motivos-tabla">
              <thead>
                <tr className="sticky-header">
                  {camposVisibles.map((field) => (
                    <th key={field.name}>{field.label}</th>
                  ))}
                  {editable && <th className="motivos-col-accion"><span className="visually-hidden">Acciones</span></th>}
                </tr>
              </thead>
              <tbody>
                {mostrarFiltroInicial || datos.length === 0 ? (
                  <tr className="motivos-fila-vacia">
                    <td colSpan={cantidadColumnas}>
                      {hayFiltros ? (
                        <div className="motivos-vacio">
                          <SearchX size={24} aria-hidden="true" />
                          <p>Ningún motivo coincide con los filtros.</p>
                          <button type="button" className="btn btn-link p-0" onClick={handleResetFilter}>
                            Limpiar filtros
                          </button>
                        </div>
                      ) : (
                        <div className="motivos-vacio">
                          <Tags size={24} aria-hidden="true" />
                          <p>Todavía no hay motivos cargados.</p>
                          {editable && (
                            <button type="button" className="btn btn-outline-dark motivos-agregar" onClick={handleAgregar}>
                              <Plus size={16} aria-hidden="true" />
                              Agregar el primero
                            </button>
                          )}
                        </div>
                      )}
                    </td>
                  </tr>
                ) : (
                  datos.map((item, index) => (
                    <tr
                      key={index}
                      onClick={() => handleRowClick(item)}
                      className={[
                        editable && "motivos-fila-editable",
                        !item.activo && "motivos-fila-inactiva",
                      ].filter(Boolean).join(" ")}
                    >
                      {camposVisibles.map((field) => {
                        const valor = item[field.name];
                        if (field.type === "date" && valor) {
                          return <td key={field.name}>{new Date(valor).toLocaleDateString('es-ES')}</td>;
                        }
                        if (field.type === "checkbox") {
                          return (
                            <td key={field.name}>
                              <span className="motivos-booleano">
                                <span className={`motivos-punto ${valor ? "motivos-punto-si" : ""}`} aria-hidden="true" />
                                {valor ? "Sí" : "No"}
                              </span>
                            </td>
                          );
                        }
                        if (field.name === "nota") {
                          return <td key={field.name}>{valor && valor.trim() !== "" ? "SI" : "NO"}</td>;
                        }
                        if (field.name === "motivo" && !item.activo) {
                          return (
                            <td key={field.name}>
                              {valor || "-"}
                              <span className="motivos-etiqueta-inactivo">Inactivo</span>
                            </td>
                          );
                        }
                        return <td key={field.name}>{valor || "-"}</td>;
                      })}
                      {editable && (
                        <td className="motivos-col-accion">
                          <button
                            type="button"
                            className="motivos-editar"
                            aria-label={`Editar ${item.motivo}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleRowClick(item);
                            }}
                          >
                            <Pencil size={16} aria-hidden="true" />
                          </button>
                        </td>
                      )}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          <div className="motivos-pie">
            <span>Mostrando {datos.length} {datos.length === 1 ? "motivo" : "motivos"}</span>
            {hayFiltros && <span className="motivos-pie-filtros">Filtros aplicados</span>}
          </div>
        </div>
      )}
    </div>
  );
};
export default ListarMotivos;
