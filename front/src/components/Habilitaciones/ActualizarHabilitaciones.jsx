import LayoutActualizar from "../../layout/LayoutActualizar";
import EditarHabilitaciones from './EditarHabilitaciones';
import ListarHabilitaciones from './ListarHabilitaciones';

const ActualizarHabilitaciones = () => {
  return (
    <LayoutActualizar
      editar={<EditarHabilitaciones />}
      listar={<ListarHabilitaciones claveFiltro="habilitaciones:actualizar" />}
      ratioEditar={25}
      ratioListar={75}
      tituloEditar="Editar Habilitaciones"
      tituloListar="Listado de Habilitaciones"
    />
  );
};

export default ActualizarHabilitaciones;
