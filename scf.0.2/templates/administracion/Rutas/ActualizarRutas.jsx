import React from 'react';
import LayoutActualizar from "../../../layout/LayoutActualizar";
import EditarRutas from './EditarRutas';
import ListarRutas from './ListarRutas';

const ActualizarRutas = () => {
  return (
    <LayoutActualizar
      editar={<EditarRutas />}
      listar={<ListarRutas />}
      ratioEditar={25}
      ratioListar={75}
      tituloEditar="Editar Rutas"
      tituloListar="Listado de Rutas"
    />
  );
};

export default ActualizarRutas;
