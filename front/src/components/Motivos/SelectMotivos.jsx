import React from "react";
import { usePostMotivosByFieldMutation } from "../../store/apiSlice"; 
import GenericSelect from "../../common/GenericSelect";

const SelectMotivos = ({ value, labelKey, onSelect,disabled, multiple }) => {
  return (
    <GenericSelect
      value={value}
      onSelect={onSelect}
      useQuery={()=>usePostMotivosByFieldMutation()} 
      valueKey="_id"
      labelKey={labelKey}
      disabled={disabled}
      placeholder="Seleccione una Opción" 
      multiple={multiple} // Habilitar selección múltiple
    />
  );
};

export default SelectMotivos;
