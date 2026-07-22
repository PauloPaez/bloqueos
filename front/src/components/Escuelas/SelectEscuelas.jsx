import React from "react";
import { usePostEscuelasByFieldMutation } from "../../store/apiSlice"; 
import GenericSelect from "../../common/GenericSelect";

const SelectEscuelas = ({ value, labelKey, onSelect,disabled, multiple }) => {
  return (
    <GenericSelect
      value={value}
      onSelect={onSelect}
      useQuery={()=>usePostEscuelasByFieldMutation()} 
      valueKey="_id"
      labelKey={labelKey}
      disabled={disabled}
      placeholder="Seleccione una Opción" 
      multiple={multiple} // Habilitar selección múltiple
    />
  );
};

export default SelectEscuelas;
