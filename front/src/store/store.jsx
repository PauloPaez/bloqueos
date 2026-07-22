import { configureStore } from "@reduxjs/toolkit";
import { objetosApi } from "./apiSlice";
import { filaSlice, accesoSlice, filtroListadoSlice} from "./appSlice";
import { modulosSlice } from "./appSlice";

export const store = configureStore({
  reducer: {
    fila: filaSlice.reducer,
    acceso: accesoSlice.reducer,
    listado: filtroListadoSlice.reducer,
    modulos: modulosSlice.reducer,
    [objetosApi.reducerPath]: objetosApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(objetosApi.middleware),
});
