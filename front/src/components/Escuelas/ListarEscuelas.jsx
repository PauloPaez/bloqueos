import React, { useState, useEffect, useCallback } from "react";
import { usePostEscuelasByFieldMutation } from "../../store/apiSlice";
import { useDispatch, useSelector } from "react-redux";
import { setModuloState, resetModulo, setFiltroListado } from "../../store/appSlice";
import FiltroEscuelas from "./FiltroEscuelas";
import { convertirMesANumero } from "../../common/meses"; 
import { API_BASE_URL, WS_BASE_URL } from "../../config/api";
import '../../common/tables.css';
import { formularioCampos } from './FormularioListar';
import Pagination from "../Pagination/Pagination";
import { Download } from "lucide-react";


const ListarEscuelas = () => {
  const dispatch = useDispatch();
  const filtroListado = useSelector((state) => state.listado.filtro);
  const [postEscuelas] = usePostEscuelasByFieldMutation();
  const [datos, setDatos] = useState([]);
  const [paginacion, setPaginacion] = useState({
        total: 0,
        page: 1,
        page_size: 10,
        total_pages: 0,
    });
  const [isLoading, setIsLoading] = useState(true);
  const [isDownloadingExcel, setIsDownloadingExcel] = useState(false);
  // Definir el filtro inicial
  const [mostrarFiltroInicial, setMostrarFiltroInicial] = useState(false);
  const filtroInicial = {};
  const postFijo = {};


  // Cargar datos iniciales

const buscarEscuelas = async (
        filtro,
        page = 1,
        page_size = paginacion.page_size,
    ) => {
        setIsLoading(true);
        try {
      const result = await postEscuelas({
                filter: filtro,
                page,
                page_size,
            }).unwrap();
            setDatos(result?.data || []);
            setPaginacion({
                total: result?.total || 0,
                page: result?.page || 1,
                page_size: result?.page_size || page_size,
                total_pages: result?.total_pages || 0,
            });
            setMostrarFiltroInicial((result?.data || []).length === 0);
        } catch (err) {
            console.error("Error fetching datos:", err);
            setDatos([]);
            setMostrarFiltroInicial(true);
        } finally {
            setIsLoading(false);
        }
    };


  useEffect(() => {
    const cargarDatosIniciales = async () => {
      setIsLoading(true);
      try {
        const filtroActual = { ...filtroInicial, ...postFijo };
        console.log("Cargando datos con filtro:", filtroActual);
        dispatch(setFiltroListado(filtroActual));
        const result = await postEscuelas({
          filter: filtroActual,
          page: 1,
          page_size: paginacion.page_size,
        }).unwrap();
        setDatos(result?.data || []);
        setPaginacion({
          total: result?.total || 0,
          page: result?.page || 1,
          page_size: result?.page_size || paginacion.page_size,
          total_pages: result?.total_pages || 0,
        });
        setMostrarFiltroInicial((result?.data || []).length === 0);
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
        dispatch(resetModulo({ modulo: 'escuelas' }));
        const filtroTransformado = { ...filtroListado };
        if (filtroTransformado.mes && typeof filtroTransformado.mes === "string") {
          const numeroMes = convertirMesANumero(filtroTransformado.mes);
          if (numeroMes) {
            filtroTransformado.mes = numeroMes;
          }
          await buscarEscuelas(
                    filtroTransformado,
                    1,
                    paginacion.page_size,
                );
        }
        try {
          const result = await postEscuelas({
            filter: filtroTransformado,
            page: 1,
            page_size: paginacion.page_size,
          }).unwrap();
          setDatos(result?.data || []);
          setPaginacion({
            total: result?.total || 0,
            page: result?.page || 1,
            page_size: result?.page_size || paginacion.page_size,
            total_pages: result?.total_pages || 0,
          });
          setMostrarFiltroInicial((result?.data || []).length === 0);
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
  }, [filtroListado]);
  const refetch = useCallback(() => {
    if (filtroListado && Object.keys(filtroListado).length > 0) {
      return postEscuelas({
        filter: filtroListado,
        page: paginacion.page,
        page_size: paginacion.page_size,
      }).unwrap()
        .then(result => {
          setDatos(result?.data || []);
          setPaginacion({
            total: result?.total || 0,
            page: result?.page || paginacion.page,
            page_size: result?.page_size || paginacion.page_size,
            total_pages: result?.total_pages || 0,
          });
        })
        .catch(err => console.error("Error recargando datos:", err));
    }
    return Promise.resolve();
  }, [filtroListado, paginacion.page, paginacion.page_size, postEscuelas]);
  // WebSocket
  useEffect(() => {
    const websocket = new WebSocket(`${WS_BASE_URL}ws/escuelas`);
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
      modulo: 'escuelas',
      nuevosDatos: {
        datos: dato,
        estadoEdicion: true,
        mostrarModal: true,
      }
    }));
  };
  const handleResetFilter = () => {
    const filtroReset = { ...filtroInicial, ...postFijo };
    dispatch(setFiltroListado(filtroReset));
    postEscuelas({
      filter: filtroReset,
      page: 1,
      page_size: paginacion.page_size,
    }).unwrap()
      .then(result => {
        setDatos(result?.data || []);
        setPaginacion({
          total: result?.total || 0,
          page: result?.page || 1,
          page_size: result?.page_size || paginacion.page_size,
          total_pages: result?.total_pages || 0,
        });
        setMostrarFiltroInicial((result?.data || []).length === 0);
      })
      .catch(err => console.error("Error recargando datos reset:", err));
  };

  const handlePageChange = (newPage) => {
        buscarEscuelas(filtroListado, newPage, paginacion.page_size);
  };

  const handlePageSizeChange = (newPageSize) => {
        buscarEscuelas(filtroListado, 1, newPageSize);
  };

  const handleDescargarExcel = async () => {
    setIsDownloadingExcel(true);
    try {
      const response = await fetch(`${API_BASE_URL}generar-excel-bloqueados`, {
        method: "POST",
        headers: {
          Accept: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "No se pudo generar el Excel");
      }

      const blob = await response.blob();
      const contentDisposition = response.headers.get("Content-Disposition") || "";
      const match = contentDisposition.match(/filename="([^"]+)"/i);
      const filename = match?.[1] || "escuelas_bloqueadas.xlsx";
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Error generando Excel:", err);
      window.alert(err.message || "Error al generar el Excel");
    } finally {
      setIsDownloadingExcel(false);
    }
  };

  if (isLoading) {
    return (
      <div className="text-center my-4">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
        <p className="mt-2">Cargando escuelas...</p>
      </div>
    );
  }
  // Filtrar campos visibles
  const camposVisibles = formularioCampos.filter(field => field.placeholder !== "no_visible");
  return (
    <div className="schools-list">
      <header className="listado-header">
        <h1 className="listado-titulo">Listado de Escuelas</h1>
        <button
          type="button"
          className="btn btn-outline-dark schools-list-download"
          onClick={handleDescargarExcel}
          disabled={isDownloadingExcel}
        >
          <Download size={16} aria-hidden="true" />
          {isDownloadingExcel ? "Generando..." : "Descargar Excel"}
        </button>
      </header>

      <FiltroEscuelas filtroInicial={filtroInicial} postFijo={postFijo} />
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
          <div className="table-container" data-pagination>
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
          <div className="table-results-summary">
            Mostrando {datos.length} de {paginacion.total} registros
          </div>
          <Pagination
                        currentPage={paginacion.page}
                        totalItems={paginacion.total}
                        pageSize={paginacion.page_size}
                        onPageChange={handlePageChange}
                        onPageSizeChange={handlePageSizeChange}
                    />
        </div>
      ) : (
        !mostrarFiltroInicial && <p>No hay datos disponibles</p>
      )}
    </div>
  );
};
export default ListarEscuelas;
