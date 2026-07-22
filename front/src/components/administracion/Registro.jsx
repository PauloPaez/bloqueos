import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import {
  usePostUsuariosMutation,
  usePostPersonasMutation,
  usePostUsuariosByFieldMutation,
  useGetRolesQuery
} from '../../store/apiSlice';

import { formularioRegistroCampos } from './FormularioRegistro';

const Registro = ({ volver }) => {
  const [postUsuarios] = usePostUsuariosMutation();
  const [postPersonas] = usePostPersonasMutation();
  const [buscarLoginByField] = usePostUsuariosByFieldMutation();

  const { data: rolesDataConAdministrador = [] } = useGetRolesQuery();
  const rolesData = rolesDataConAdministrador.filter(
    rol => rol.rol !== "Administrador"
  );

  const {
    register,
    handleSubmit,
    watch,
    reset,
    setValue,
    formState: { errors }
  } = useForm();

  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState(null);

  // LOGIN dinámico
  const [loginSearchTerm, setLoginSearchTerm] = useState('');
  const [loginEncontrados, setLoginEncontrados] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [loginDuplicado, setLoginDuplicado] = useState(false);

  // PASSWORD
  const [claveCoincide, setClaveCoincide] = useState(false);
  const [claveTocada, setClaveTocada] = useState(false);
  const [reclaveTocada, setReclaveTocada] = useState(false);

  const clave = watch("clave");
  const reclave = watch("reclave");

  useEffect(() => {
    if (reclaveTocada && clave && reclave) {
      setClaveCoincide(clave === reclave);
    } else {
      setClaveCoincide(false);
    }
  }, [clave, reclave, reclaveTocada]);

  // 🔎 Buscar login
  useEffect(() => {
    const searchLogin = async () => {
      if (loginSearchTerm.length < 2) {
        setLoginEncontrados([]);
        setLoginDuplicado(false);
        return;
      }

      setSearchLoading(true);
      try {
        const result = await buscarLoginByField({ login: loginSearchTerm }).unwrap();

        if (result?.length > 0) {
          setLoginEncontrados(result);

          const existeExacto = result.some(item =>
            item.login.toLowerCase() === loginSearchTerm.toLowerCase()
          );

          const haySimilitud = result.some(item =>
            item.login.toLowerCase().includes(loginSearchTerm.toLowerCase()) ||
            loginSearchTerm.toLowerCase().includes(item.login.toLowerCase())
          );

          setLoginDuplicado(existeExacto || haySimilitud);
        } else {
          setLoginDuplicado(false);
        }
      } catch (error) {
        console.error("Error login:", error);
        setLoginDuplicado(false);
      } finally {
        setSearchLoading(false);
      }
    };

    const t = setTimeout(searchLogin, 500);
    return () => clearTimeout(t);
  }, [loginSearchTerm, buscarLoginByField]);

  const handleLoginChange = (e) => {
    const value = e.target.value;
    setLoginSearchTerm(value);
    setValue('login', value, { shouldValidate: false });

    if (value.length < 2) setLoginDuplicado(false);
  };

  const handleClaveChange = () => setClaveTocada(true);
  const handleReclaveChange = () => setReclaveTocada(true);

  // 📦 Submit
  const onSubmit = async (data) => {
    if (loginDuplicado) {
      setMensaje({ tipo: 'danger', texto: 'El login ya existe o es similar' });
      return;
    }

    if (data.clave !== data.reclave) {
      setMensaje({ tipo: 'danger', texto: 'Las contraseñas no coinciden' });
      return;
    }

    setLoading(true);
    setMensaje(null);

    try {
      await postUsuarios({
        nombre: data.nombre,
        apellido: data.apellido,
        login: data.login,
        clave: data.clave,
        empresas: [data.empresa],
        roles: [data.tipo_comercio],
        activo: true
      }).unwrap();

      await postPersonas({
        nombre: data.nombre,
        apellido: data.apellido,
        dni: data.dni,
        celular: data.celular,
        calle_nro: data.calle_nro,
        barrio: data.barrio,
        departamento: data.departamento,
        provincia: data.provincia,
        correo: data.correo,
        tipo_comercio: data.tipo_comercio,
        login_cnx: data.login,
        empresa_cnx: data.empresa,
        activo: true
      }).unwrap();

      setMensaje({ tipo: 'success', texto: 'Cuenta creada correctamente' });

      reset();
      setLoginSearchTerm('');
      setLoginDuplicado(false);
      setClaveCoincide(false);
      setClaveTocada(false);
      setReclaveTocada(false);

    } catch {
      setMensaje({ tipo: 'danger', texto: 'Error al registrar usuario' });
    } finally {
      setLoading(false);
    }
  };

  // 🔧 Helpers
  const getCamposPorColumna = (col) =>
    formularioRegistroCampos.filter(f => f.col === col);

  const renderInput = (field) => {
    if (!field) return null;

    const rules = field.required
      ? { required: `El campo ${field.label} es requerido` }
      : {};

    if (field.type === "select") {
      return (
        <div key={field.name} className="mb-2">
          <label className="form-label">{field.label}</label>
          <select
            className={`form-control ${errors[field.name] ? 'is-invalid' : ''}`}
            {...register(field.name, rules)}
            defaultValue=""
          >
            <option value="" disabled>Seleccione</option>
            {rolesData.map((rolObj, i) => (
              <option key={i} value={rolObj.rol}>{rolObj.rol}</option>
            ))}
          </select>
          {errors[field.name] && (
            <div className="invalid-feedback d-block">
              {errors[field.name].message}
            </div>
          )}
        </div>
      );
    }

    if (field.name === "clave") {
      return (
        <div key="clave" className="mb-2">
          <label className="form-label">Clave</label>
          <input
            type="password"
            className={`form-control ${errors.clave ? 'is-invalid' : claveTocada ? 'is-valid' : ''}`}
            {...register("clave", {
              required: "La clave es requerida",
              onChange: handleClaveChange
            })}
          />
        </div>
      );
    }

    if (field.name === "reclave") {
      return (
        <div key="reclave" className="mb-2">
          <label className="form-label">Repetir clave</label>
          <input
            type="password"
            className={`form-control ${reclaveTocada ? (claveCoincide ? 'is-valid' : 'is-invalid') : ''}`}
            {...register("reclave", {
              required: "Debe repetir la clave",
              validate: v => v === clave || "No coinciden",
              onChange: handleReclaveChange
            })}
          />
        </div>
      );
    }

    return (
      <Input
        key={field.name}
        label={field.label}
        type={field.type}
        {...register(field.name, rules)}
        error={errors[field.name]?.message}
      />
    );
  };

  return (
    <div className="d-flex justify-content-center align-items-center min-vh-100"
      style={{ background: 'linear-gradient(135deg,#667eea,#764ba2)' }}
    >
      <div className="card p-4" style={{ maxWidth: 900, width: '100%' }}>
        <h3 className="text-center mb-4">Registro</h3>

        {mensaje && (
          <div className={`alert alert-${mensaje.tipo}`}>
            {mensaje.texto}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="row g-3">

            <div className="col-md-4">
              {getCamposPorColumna(1).map(renderInput)}
            </div>

            <div className="col-md-4">

              {/* LOGIN custom */}
              <div className="mb-2 position-relative">
                <label className="form-label">Login</label>
                <input
                  className={`form-control ${loginDuplicado ? 'is-invalid' : ''}`}
                  value={loginSearchTerm}
                  onChange={handleLoginChange}
                />
                {loginDuplicado && (
                  <div className="invalid-feedback d-block">
                    Login ya existe
                  </div>
                )}
              </div>

              {getCamposPorColumna(2)
                .filter(f => f.name !== "login")
                .map(renderInput)}

            </div>

            <div className="col-md-4">
              {getCamposPorColumna(3).map(renderInput)}
            </div>

          </div>

          <div className="d-flex justify-content-between mt-4">
            <button type="button" className="btn btn-outline-secondary" onClick={volver}>
              Cancelar
            </button>

            <button
              className="btn btn-primary"
              disabled={loading || loginDuplicado}
            >
              {loading ? 'Registrando...' : 'Enviar'}
            </button>
          </div>

        </form>
      </div>
    </div>
  );
};

const Input = ({ label, error, ...props }) => (
  <div className="mb-2">
    <label className="form-label">{label}</label>
    <input className={`form-control ${error ? 'is-invalid' : ''}`} {...props} />
    {error && <div className="invalid-feedback d-block">{error}</div>}
  </div>
);

export default Registro;