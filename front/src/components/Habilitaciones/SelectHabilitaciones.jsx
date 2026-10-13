import React from "react";
import { usePostHabilitacionesByFieldMutation } from "../../store/apiSlice"; 
import GenericSelect from "../../common/GenericSelect";

const SelectHabilitaciones = ({ value, labelKey, onSelect,disabled, multiple }) => {
  return (
    <GenericSelect
      value={value}
      onSelect={onSelect}
      useQuery={()=>usePostHabilitacionesByFieldMutation()} 
      valueKey="_id"
      labelKey={labelKey}
      disabled={disabled}
      placeholder="Seleccione una Opción" 
      multiple={multiple} // Habilitar selección múltiple
    />
  );
};

export default SelectHabilitaciones;
