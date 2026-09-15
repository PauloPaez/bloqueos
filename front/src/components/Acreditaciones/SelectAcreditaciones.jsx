import React from "react";
import { usePostAcreditacionesByFieldMutation } from "../../store/apiSlice"; 
import GenericSelect from "../../common/GenericSelect";

const SelectAcreditaciones = ({ value, labelKey, onSelect,disabled, multiple }) => {
  return (
    <GenericSelect
      value={value}
      onSelect={onSelect}
      useQuery={()=>usePostAcreditacionesByFieldMutation()} 
      valueKey="_id"
      labelKey={labelKey}
      disabled={disabled}
      placeholder="Seleccione una Opción" 
      multiple={multiple} // Habilitar selección múltiple
    />
  );
};

export default SelectAcreditaciones;
