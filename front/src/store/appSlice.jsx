import { createSlice } from "@reduxjs/toolkit";
export const filaSlice = createSlice({
    name: "fila",
    initialState: {
        elegida: {}
    },
    reducers: {
        setFila: (state, action) => {
            state.elegida = { ...state.elegida, ...action.payload }
        },
        setFilaSubdocumento: (state, action) => {
            const { subdoc, field, value } = action.payload;
            state.elegida[subdoc][field] = value;
        },
        resetFila: (state) => {
            state.elegida = {}; // Limpia el estado de fila seleccionada
        }
    }
});
export const { setFila, setFilaSubdocumento, resetFila } = filaSlice.actions;
export const asignacionSlice = createSlice({
    name: "asignacion",
    initialState: {
        elegida: {}
    },
    reducers: {
        setAsignacion: (state, action) => {
            if (Array.isArray(action.payload.archivos)) {
                // Concatenar el array de archivos si existe
                state.elegida.archivos = [
                    ...(state.elegida.archivos || []),
                    ...action.payload.archivos
                ];
            } else {
                // Combina el resto de los valores en el estado elegida
                state.elegida = { ...state.elegida, ...action.payload };
            }
        },
        setAsignacionSubdocumento: (state, action) => {
            const { subdoc, field, value } = action.payload;
            if (state.elegida[subdoc]) {
                state.elegida[subdoc][field] = value;
            }
        }
    }
});
export const { setAsignacion, setAsignacionSubdocumento } = asignacionSlice.actions;
export const accesoSlice = createSlice({
    name: "acceso",
    initialState: {
        user: { login: "", opciones: [] }, // Estructura inicial correcta
    },
    reducers: {
        setAcceso: (state, action) => {
            state.user = action.payload || { login: "", opciones: [] };
        },
        resetAcceso: (state) => {
            state.user = { login: "", opciones: [] };
        }
    }
});
export const { setAcceso, resetAcceso } = accesoSlice.actions;
export const filtroListadoSlice = createSlice({
    name: "listado", // Nombre del slice
    initialState: {
        filtro: {},
    },
    reducers: {
        // Reducer para actualizar el estado `filtro`
        setFiltroListado: (state, action) => {
            state.filtro = { ...action.payload };
        },
        resetFiltroListado: (state) => {
            state.filtro = {};
        },
    },
});
export const { setFiltroListado, resetFiltroListado } = filtroListadoSlice.actions;
export const modulosSlice = createSlice({
    name: 'modulos',
    initialState: {
        // Estructura de datos para cada módulo
        escuelas: {
            datos: null,
            filtros: {},
            estadoEdicion: false,
            mostrarModal: false,
        },
        personas: {
            datos: null,
            filtros: {},
            estadoEdicion: false,
            mostrarModal: false,
        },
    },
    reducers: {
        // Reducer genérico para actualizar cualquier estado de módulo
        setModuloState: (state, action) => {
            const { modulo, nuevosDatos } = action.payload;
            state[modulo] = { ...state[modulo], ...nuevosDatos };
        },
        // Reducer para resetear un módulo
        resetModulo: (state, action) => {
            const { modulo } = action.payload;
            state[modulo] = {
                datos: null,
                filtros: {},
                estadoEdicion: false,
                mostrarModal: false,
            };
            // Puedes añadir propiedades específicas para cada módulo en el reset si es necesario
        }
    }
});
export const {
    setModuloState,
    resetModulo
} = modulosSlice.actions;
