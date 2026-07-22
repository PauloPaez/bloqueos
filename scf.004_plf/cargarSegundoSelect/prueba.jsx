import React, { useEffect, useState, useCallback } from 'react';

import { useForm } from 'react-hook-form';

import { usePostNro_notasMutation, usePatchNro_notasMutation } from '../../store/apiSlice';

import { useGetDistinctTipo_notasQuery } from '../../store/apiSlice';

import { useSelector, useDispatch } from 'react-redux';

import { usePostTipo_notasByFieldMutation } from'../../store/apiSlice';
import { resetModulo } from '../../store/appSlice';



const EditarNro_notas = () => {

  const [postNro_notas] = usePostNro_notasMutation();

  // const [patchNro_notas] = usePatchNro_notasMutation(); // Importar la mutación PATCH

  const dispatch = useDispatch();

  const { data: Categorias = [] } = useGetDistinctTipo_notasQuery('categoria');

  const user = useSelector((state) => state.acceso.user);



  // Resetear la fila seleccionada al montar el componente

  useEffect(() => {

    dispatch(resetModulo({ modulo: 'nro_notas' }));

  }, [dispatch]);



  const filaSeleccionada = useSelector((state) => state.modulos.nro_notas).datos;    

 const [Tipos, setTipos] = useState([]);
 const [recuperarTipos] = usePostTipo_notasByFieldMutation();




  const [isActualizarDisabled, setIsActualizarDisabled] = useState(true);

  const [isEnviarDisabled, setIsEnviarDisabled] = useState(false);



  const { register, handleSubmit, setValue, reset, watch } = useForm({

    defaultValues: {

      nro_notas: [{}],

    },

  });



  const formFields = [

	{name: 'numero', label: 'Número', placeholder: 'Número', type: 'number'},

	{name: 'categoria', label: 'Categoria', placeholder: 'Categoria', type: 'select', optionsKey: 'categorias'},

	{name: 'tipo', label: 'Tipo', placeholder: 'Tipo', type: 'select', optionsKey: 'tipos'},

	{name: 'fecha', label: 'Fecha', placeholder: 'Fecha', type: 'date'},

	{name: 'login', label: 'login', placeholder: 'no_visible', type: 'text'},

	{name: 'empresa', label: 'Empresa', placeholder: 'no_visible', type: 'text'},

	{name: 'activo', label: 'Activo', placeholder: 'Activo', type: 'checkbox'},

  ];

const datosSelect = {

	'categorias': Categorias,

    'tipos': Tipos
};





  useEffect(() => {

    if (filaSeleccionada?.id) {

      setIsActualizarDisabled(false);

      setIsEnviarDisabled(true);

      formFields.forEach((field) => {

        if (field.type === 'date' && filaSeleccionada[field.name]) {

          // Convertir el valor datetime a date

          const fechaFormateada = filaSeleccionada[field.name].split('T')[0];

          setValue(`nro_notas.0.${field.name}`, fechaFormateada);

        } else {

          setValue(`nro_notas.0.${field.name}`, filaSeleccionada[field.name] || '');

        }

      });

    } else {

      setIsActualizarDisabled(true);

      setIsEnviarDisabled(false);

      reset({ nro_notas: [{}] });

    }

  }, [filaSeleccionada]);





    











const categoriaSeleccionado = watch('nro_notas!.0.categoria')
    const cargarTipos = useCallback(async (categoria) => {
        if (!categoria) {
           setTipos([]);
            return;
        }
        try {
            const result = await recuperarTipos({ categoria }).unwrap();
            const tiposUnicos = [...new Set(
                result
                    .filter(item => item.tipo)
                    .map(item => item.tipo.toString().trim())
            )];
            setTipos(tiposUnicos);
        } catch (error) {
            console.error("Error al cargar tipos:", error);
            setTipos([]);
        }
    }, [recuperarTipos]);
    useEffect(() => {
        console.log(categoriaSeleccionado)
        cargarTipos(categoriaSeleccionado);
    }, [categoriaSeleccionado, cargarTipos]);

  const onSubmit = async (data) => {

    try {

          const nro_notasData = {

        	...data.nro_notas[0],

        	empresa: user.empresa,

        	login: user.login,

          activo: true

      		};

      const response = await postNro_notas(nro_notasData).unwrap();

      reset();

    } catch (error) {

      console.error('Error al enviar los datos (POST):', error);

    }

  };



  const onActualizar = async (data) => {

    try {

      const updatedData = { id: filaSeleccionada.id, ...data.nro_notas[0],login: user.login };

      const response = await patchNro_notas(updatedData).unwrap();

      reset();

      dispatch(resetModulo({ modulo: 'nro_notas' })); 

      setIsActualizarDisabled(true);

      setIsEnviarDisabled(false);

    } catch (error) {

      console.error('Error al actualizar los datos (PATCH):', error);

    }

  };



  const handleReset = () => {

    reset();

    dispatch(resetModulo({ modulo: 'empleado' }));

    setIsActualizarDisabled(true);

    setIsEnviarDisabled(false);

  };



return (

  <form style={{ padding: '20px', backgroundColor: isActualizarDisabled ? '#ffffff' : '#fcf4dd', }}>

    {formFields

      .filter(field => field.placeholder !== 'no_visible')

      .map((field) => {

        const fieldProps = {

          ...register(`nro_notas.0.${field.name}`),

          disabled: field.disabled,

        };



        return (

          <div key={field.name} className={`mb-3 ${field.type === 'checkbox' ? 'form-check' : ''}`}>

            {field.type !== 'checkbox' && <label className='form-label'>{field.label}</label>}



            {(() => {

              switch(field.type) {

                case 'select':

                  return (

                    <select className='form-control' {...fieldProps}>

                      <option value=''>Seleccione {field.label.toLowerCase()}</option>

                      {(datosSelect[field.optionsKey] || []).map((opcion, index) => (

                        <option key={index} value={opcion}>{opcion}</option>

                      ))}

                    </select>

                  );

                

                case 'checkbox':

                  return (

                    <>

                      <input

                        type='checkbox'

                        className='form-check-input'

                        {...fieldProps}

                      />

                      <label className='form-check-label'>{field.label}</label>

                    </>

                  );

                

                default:

                  return (

                    <input

                      type={field.type}

                      className='form-control'

                      {...fieldProps}

                    />

                  );

              }

            })()}

          </div>

        );

      })}



    <div className='d-flex justify-content-between mt-3'>

      <button

        type='button'

        className='btn btn-outline-primary'

        disabled={isEnviarDisabled}

        onClick={handleSubmit(onSubmit)}

      >

        Grabar

      </button>

      

      <button

        type='button'

        className='btn btn-outline-warning'

        disabled={isActualizarDisabled}

        onClick={handleSubmit(onActualizar)}

      >

        Actualizar

      </button>

      

      <button 

        type='button' 

        className='btn btn-outline-danger' 

        onClick={handleReset}

      >

        Reset

      </button>

    </div>

  </form>

);

};



export default EditarNro_notas;





