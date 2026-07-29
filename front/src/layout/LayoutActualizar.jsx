// components/layout/LayoutActualizar.jsx
import React from "react";

const LayoutActualizar = ({
  editar,
  listar,
  ratioEditar = 0,
  ratioListar = 100,
  ocultarEditar = false,
  tituloEditar,
  tituloListar,
}) => {
  return (
    <div
      className={`pantalla-container ${
        ocultarEditar ? "solo-listar" : ""
      }`}
    >
      {!ocultarEditar && (
        <div
          className="editar-modelo"
          style={{ flexBasis: `${ratioEditar}%` }}
        >
          {tituloEditar && <h5 className="layout-titulo">{tituloEditar}</h5>}
          {editar}
        </div>
      )}

      <div
        className="listar-modelo"
        style={{ flexBasis: `${ratioListar}%` }}
      >
        {tituloListar && <h5 className="layout-titulo">{tituloListar}</h5>}
        {listar}
      </div>
    </div>
  );
};

export default LayoutActualizar;

