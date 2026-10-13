import React from 'react';
import LayoutActualizar from "../../layout/LayoutActualizar";
import EditarPersonas from './EditarPersonas';
import ListarPersonas from './ListarPersonas';

const ActualizarPersonas = () => {
  return (
    <LayoutActualizar
      editar={<EditarPersonas />}
      listar={<ListarPersonas />}
      ratioEditar={25}
      ratioListar={75}
      tituloEditar="Editar Personas"
      tituloListar="Listado de Personas"
    />
  );
};

export default ActualizarPersonas;
