import { usePostRolesByFieldMutation } from "../../../store/apiSlice"; 
import GenericSelect from "../../../common/GenericSelect";

const SelectRoles = ({ value, onSelect }) => {
  return (
    <GenericSelect
      value={value}
      onSelect={onSelect}
      useQuery={()=>usePostRolesByFieldMutation()} 
      valueKey="_id"
      labelKey="rol"
      placeholder="Seleccione uno o más roles"
      label="Roles"
      multiple // Habilitar selección múltiple
    />
  );
};

export default SelectRoles;
