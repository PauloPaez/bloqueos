import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import Navbar from "./Navbar";
// Importar todos los componentes
import ActualizarEscuelas from "../Escuelas/ActualizarEscuelas";
import ListarEscuelas from "../Escuelas/ListarEscuelas";
import ActualizarUsuarios from "./Usuarios/ActualizarUsuarios";
import ListarUsuarios from "./Usuarios/ListarUsuarios";
import ActualizarRoles from "./Roles/ActualizarRoles";
import ListarRoles from "./Roles/ListarRoles";
import ActualizarRutas from "./Rutas/ActualizarRutas";
import ListarRutas from "./Rutas/ListarRutas";
import ActualizarPersonas from "../Personas/ActualizarPersonas";
import ListarPersonas from "../Personas/ListarPersonas";
const ProtectedRoutes = () => {
  const accesos = useSelector((state) => state.acceso.user);

  // Si no hay accesos, redirige al login
  if (!accesos || !accesos.opciones || accesos.opciones.length === 0) {
    return <Navigate to="/login" />;
  }

  // Mapa de rutas a componentes
  const componentMap = {
    "/Escuelas/ActualizarEscuelas": ActualizarEscuelas,
    "/Escuelas/ListarEscuelas": ListarEscuelas,
    "/Usuarios/ActualizarUsuarios": ActualizarUsuarios,
    "/Usuarios/ListarUsuarios": ListarUsuarios,
    "/Roles/ActualizarRoles": ActualizarRoles,
    "/Roles/ListarRoles": ListarRoles,
    "/Rutas/ActualizarRutas": ActualizarRutas,
    "/Rutas/ListarRutas": ListarRutas,
    "/Personas/ActualizarPersonas": ActualizarPersonas,
    "/Personas/ListarPersonas": ListarPersonas,
  };

  return (
    <>
      {/* Navbar se renderiza solo una vez */}
      <Navbar />
      <Routes>
        {accesos.opciones.map((opcion) => {
          const Component = componentMap[opcion.path] || (() => <div>Página no encontrada</div>);
          return <Route key={opcion.path} path={opcion.path} element={<Component />} />;
        })}
        {/* Redirige a la primera ruta disponible si no se encuentra la ruta */}
        <Route
          path="*"
          element={<Navigate to={accesos.opciones[0]?.path || "/login"} />}
        />
      </Routes>
    </>
  );
};

export default ProtectedRoutes;
