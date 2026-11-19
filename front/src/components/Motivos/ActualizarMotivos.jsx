import LayoutActualizar from "../../layout/LayoutActualizar";
import EditarMotivos from './EditarMotivos';
import ListarMotivos from './ListarMotivos';

const ActualizarMotivos = () => {
  return (
    <>
      <LayoutActualizar
        ocultarEditar={true}
        listar={<ListarMotivos claveFiltro="motivos:actualizar" editable />}
      />

      <EditarMotivos />
    </>
  );
};

export default ActualizarMotivos;
