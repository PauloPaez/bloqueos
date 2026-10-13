import React, { useState, useEffect, useCallback, useMemo, useRef } from "react";
import { usePostPersonasByFieldMutation } from "../../store/apiSlice";
import { useDispatch, useSelector } from "react-redux";
import { setModuloState, resetModulo, setFiltroListado } from "../../store/appSlice";
import FiltroPersonas from "./FiltroPersonas";
import { convertirMesANumero } from "../../common/meses";
import { WS_BASE_URL } from "../../config/api";
import '../../common/tables.css';

import { formularioCampos } from './FormularioListar';

const ListarPersonas = () => {

  const dispatch = useDispatch();
  const filtroListado = useSelector((state) => state.listado.filtro);

  const [postPersonas] = usePostPersonasByFieldMutation();
  const [datos, setDatos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [mostrarFiltroInicial, setMostrarFiltroInicial] = useState(false);

  const filtroInicial = useMemo(() => ({}), []);
  const postFijo = useMemo(() => ({}), []); // 👈 respetamos tu lógica actual

  const filtroListadoRef = useRef(filtroListado);
  useEffect(() => {
    filtroListadoRef.current = filtroListado;
  }, [filtroListado]);

  const normalizarFiltro = useCallback((filtro) => {
    const filtroTransformado = { ...(filtro ?? {}) };

    if (filtroTransformado.mes && typeof filtroTransformado.mes === "string") {
      const numeroMes = convertirMesANumero(filtroTransformado.mes);
      if (numeroMes) filtroTransformado.mes = numeroMes;
    }

    return filtroTransformado;
  }, []);

  const refetch = useCallback(() => {
    const filtroActual = filtroListadoRef.current;
    const filtroConsulta = normalizarFiltro(
      filtroActual && typeof filtroActual === "object"
        ? filtroActual
        : { ...filtroInicial, ...postFijo }
    );

    return postPersonas(filtroConsulta).unwrap()
      .then((result) => {
        setDatos(result || []);
        setMostrarFiltroInicial((result?.length ?? 0) === 0);
      })
      .catch((err) => {
        console.error("Error refetch:", err);
        setDatos([]);
        setMostrarFiltroInicial(true);
      });
  }, [filtroInicial, normalizarFiltro, postFijo, postPersonas]);

  // 🔹 carga inicial (igual catalogos)
  useEffect(() => {
    const cargarDatos = async () => {
      setIsLoading(true);
      try {
        const filtroActual = { ...filtroInicial, ...postFijo };
        dispatch(setFiltroListado(filtroActual));

        const result = await postPersonas(filtroActual).unwrap();
        setDatos(result || []);
        setMostrarFiltroInicial(result?.length === 0);

      } catch (err) {
        console.error("Error inicial:", err);
        setDatos([]);
        setMostrarFiltroInicial(true);
      } finally {
        setIsLoading(false);
      }
    };

    cargarDatos();
  }, [dispatch, filtroInicial, postFijo, postPersonas]);

  // 🔹 cambios de filtro
  useEffect(() => {
    if (filtroListado && Object.keys(filtroListado).length > 0) {

      const aplicarFiltro = async () => {
        setIsLoading(true);
        dispatch(resetModulo({ modulo: 'empleado' }));

        const filtroTransformado = { ...filtroListado };

        if (filtroTransformado.mes && typeof filtroTransformado.mes === "string") {
          const numeroMes = convertirMesANumero(filtroTransformado.mes);
          if (numeroMes) filtroTransformado.mes = numeroMes;
        }

        try {
          const result = await postPersonas(filtroTransformado).unwrap();
          setDatos(result || []);
          setMostrarFiltroInicial(result?.length === 0);

        } catch (err) {
          console.error("Error filtro:", err);
          setDatos([]);
          setMostrarFiltroInicial(true);
        } finally {
          setIsLoading(false);
        }
      };

      aplicarFiltro();
    }
  }, [dispatch, filtroListado, postPersonas]);

  // 🔹 websocket
  useEffect(() => {
    const websocket = new WebSocket(`${WS_BASE_URL}ws/personas`);

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
      modulo: 'personas',
      nuevosDatos: {
        datos: dato,
        estadoEdicion: true
      }
    }));
  };

  const handleResetFilter = () => {
    const filtroReset = { ...filtroInicial, ...postFijo };

    dispatch(setFiltroListado(filtroReset));

    postPersonas(filtroReset).unwrap()
      .then(result => {
        setDatos(result || []);
        setMostrarFiltroInicial(result?.length === 0);
      })
      .catch(err => console.error("Error reset:", err));
  };

  if (isLoading) {
    return (
      <div className="text-center my-4">
        <div className="spinner-border text-primary" />
        <p>Cargando personas...</p>
      </div>
    );
  }

  // 🔥 MISMA LÓGICA QUE CATALOGOS
  const camposVisibles = formularioCampos.filter(
    field => field.placeholder !== "no_visible"
  );

  return (
    <div>

      <FiltroPersonas filtroInicial={filtroInicial} postFijo={postFijo} />

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
                        return (
                          <td key={field.name}>
                            {new Date(valor).toLocaleDateString('es-ES')}
                          </td>
                        );
                      }

                      if (typeof valor === "boolean") {
                        return (
                          <td key={field.name}>
                            {valor ? "SI" : "NO"}
                          </td>
                        );
                      }

                      if (field.name === "nota") {
                        return (
                          <td key={field.name}>
                            {valor && valor.trim() !== "" ? "SI" : "NO"}
                          </td>
                        );
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

export default ListarPersonas;
