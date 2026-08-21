import { useCallback, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  setFiltroListadoPorClave,
  resetFiltroListadoPorClave,
  limpiarFiltroListadoPorClave,
} from "../store/appSlice";

const EMPTY_FILTER = {};
const EMPTY_VALUES = {};

/**
 * Estado común de filtros para cualquier listado.
 *
 * La clave identifica al listado y evita que dos recursos compartan filtros.
 * El hook mantiene la implementación de Redux fuera de los componentes de
 * cada módulo.
 */
export const useFiltroListado = (
  claveFiltro = "default",
  { limpiarAlDesmontar = false } = {}
) => {
  const dispatch = useDispatch();
  const filtroGuardado = useSelector(
    (state) => state.listado.filtrosPorClave?.[claveFiltro]
  );
  const valoresGuardados = useSelector(
    (state) => state.listado.valoresFiltrosPorClave?.[claveFiltro]
  );

  const aplicarFiltro = useCallback(
    (filtro, valores) => {
      dispatch(
        setFiltroListadoPorClave({
          clave: claveFiltro,
          filtro,
          valores,
        })
      );
    },
    [claveFiltro, dispatch]
  );

  const resetearFiltro = useCallback(
    (filtro = {}) => {
      dispatch(
        resetFiltroListadoPorClave({
          clave: claveFiltro,
          filtro,
        })
      );
    },
    [claveFiltro, dispatch]
  );

  useEffect(() => {
    if (!limpiarAlDesmontar) return undefined;

    return () => {
      dispatch(limpiarFiltroListadoPorClave({ clave: claveFiltro }));
    };
  }, [claveFiltro, dispatch, limpiarAlDesmontar]);

  return {
    filtro: filtroGuardado ?? EMPTY_FILTER,
    filtroGuardado,
    valores: valoresGuardados ?? EMPTY_VALUES,
    guardarFiltro: aplicarFiltro,
    resetearFiltro,
  };
};

export default useFiltroListado;
