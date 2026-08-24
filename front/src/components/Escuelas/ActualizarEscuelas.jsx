import LayoutActualizar from "../../layout/LayoutActualizar";
import EditarEscuelas from "./EditarEscuelas";
import ListarEscuelas from "./ListarEscuelas";

const ActualizarEscuelas = () => {
  return (
    <>
      <LayoutActualizar
        ocultarEditar={true}
        listar={<ListarEscuelas claveFiltro="escuelas:actualizar" />}
      />

      <EditarEscuelas />
    </>
  );
};

export default ActualizarEscuelas;
