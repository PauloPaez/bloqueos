// src/store/apiSlice.jsx
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_BASE_URL } from "../config/api";
export const objetosApi = createApi({
    reducerPath: "objetosApi",
 //   baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:8000/" }),
    baseQuery: fetchBaseQuery({ baseUrl: API_BASE_URL }),
    tagTypes: ["Usuarios","Roles","Rutas","Login","Personas","Pedidos","Ofertas","Escuelas","Motivos",],
    endpoints: (builder) => ({
	getMotivos: builder.query({ 
    		query: () => "motivos/",
    		providesTags: ["Motivos"],
		}),
	getMotivosById: builder.query({
		query: (id) => `motivos/${id}/`, // Ruta con el parámetro dinámico `id`
		providesTags: (result, error, id) => [{ type: "Motivos", id }],
	}),
	postMotivosByField: builder.mutation({
		query: (filter) => ({
			url: "motivos/search/",
			method: "POST",
			body: filter, // Enviar el filtro como un objeto
		}),
		providesTags: (result, error, filter) => [{ type: "Motivos", filter }],
		}),		
    postMotivos: builder.mutation({ 
        	query: (nuevoDatos) => ({
        	    url: "motivos/",
        	    method: "POST",
        	    body: nuevoDatos,
			}),
    	    invalidatesTags: ["Motivos"],
		}),
	putMotivos: builder.mutation({ 
    		query: (datos) => ({
        		url: "motivos/",
        		method: "PUT",
        		body: datos,
			}),
    		invalidatesTags: ["Motivos"],
		}),
	patchMotivos: builder.mutation({ 
    		query: (datos) => ({
        		url: "motivos/",
        		method: "PATCH",
        		body: datos,
			}),
    		invalidatesTags: ["Motivos"],
		}),
    getDistinctMotivos: builder.query({
            query: (campo) => {
                const url = `motivos/distinct/${campo}/`;
                console.log('URL generada:', url); // Verifica que sea correcta
                return url;
                },
                providesTags: ["Motivos"],
            }),
	getEscuelas: builder.query({ 
    		query: () => "escuelas/",
    		providesTags: ["Escuelas"],
		}),
	getEscuelasById: builder.query({
		query: (id) => `escuelas/${id}/`, // Ruta con el parámetro dinámico `id`
		providesTags: (result, error, id) => [{ type: "Escuelas", id }],
	}),
	postEscuelasByField: builder.mutation({
			query: ({ filter = {}, page = 1, page_size = 10 } = {}) => ({
			url: `escuelas/search/?page=${page}&page_size=${page_size}`,
			method: "POST",
			body: filter, // Enviar el filtro como un objeto
		}),
		providesTags: (result, error, filter) => [{ type: "Escuelas", filter }],
		}),		
    postEscuelas: builder.mutation({ 
        	query: (nuevoDatos) => ({
        	    url: "escuelas/",
        	    method: "POST",
        	    body: nuevoDatos,
			}),
    	    invalidatesTags: ["Escuelas"],
		}),
	putEscuelas: builder.mutation({ 
    		query: (datos) => ({
        		url: "escuelas/",
        		method: "PUT",
        		body: datos,
			}),
    		invalidatesTags: ["Escuelas"],
		}),
	patchEscuelas: builder.mutation({ 
    		query: (datos) => ({
        		url: "escuelas/",
        		method: "PATCH",
        		body: datos,
			}),
    		invalidatesTags: ["Escuelas"],
		}),
    getDistinctEscuelas: builder.query({
            query: (campo) => {
                const url = `escuelas/distinct/${campo}/`;
                console.log('URL generada:', url); // Verifica que sea correcta
                return url;
                },
                providesTags: ["Escuelas"],
            }),
	getPersonas: builder.query({ 
    		query: () => "personas/",
    		providesTags: ["Personas"],
		}),
	getPersonasById: builder.query({
		query: (id) => `personas/${id}/`, // Ruta con el parámetro dinámico `id`
		providesTags: (result, error, id) => [{ type: "Personas", id }],
	}),
	postPersonasByField: builder.mutation({
		query: (filter) => ({
			url: "personas/search/",
			method: "POST",
			body: filter, // Enviar el filtro como un objeto
		}),
		providesTags: (result, error, filter) => [{ type: "Personas", filter }],
		}),		
    postPersonas: builder.mutation({ 
        	query: (nuevoDatos) => ({
        	    url: "personas/",
        	    method: "POST",
        	    body: nuevoDatos,
			}),
    	    invalidatesTags: ["Personas"],
		}),
	putPersonas: builder.mutation({ 
    		query: (datos) => ({
        		url: "personas/",
        		method: "PUT",
        		body: datos,
			}),
    		invalidatesTags: ["Personas"],
		}),
	patchPersonas: builder.mutation({ 
    		query: (datos) => ({
        		url: "personas/",
        		method: "PATCH",
        		body: datos,
			}),
    		invalidatesTags: ["Personas"],
		}),
    getDistinctPersonas: builder.query({
            query: (campo) => {
                const url = `personas/distinct/${campo}/`;
                console.log('URL generada:', url); // Verifica que sea correcta
                return url;
                },
                providesTags: ["Personas"],
            }),
	postLoginByField: builder.mutation({
			query: (filter) => ({
				url: "login/",
				method: "POST",
				body: filter, // Enviar el filtro como un objeto
			}),
			providesTags: (result, error, filter) => [{ type: "Login", filter }],
		}),		
	getRutas: builder.query({ 
    		query: () => "rutas/",
    		providesTags: ["Rutas"],
		}),
	getRutasById: builder.query({
		query: (id) => `rutas/${id}/`, // Ruta con el parámetro dinámico `id`
		providesTags: (result, error, id) => [{ type: "Rutas", id }],
	}),
	postRutasByField: builder.mutation({
		query: (filter) => ({
			url: "rutas/search/",
			method: "POST",
			body: filter, // Enviar el filtro como un objeto
		}),
		providesTags: (result, error, filter) => [{ type: "Rutas", filter }],
		}),		
    postRutas: builder.mutation({ 
        	query: (nuevoDatos) => ({
        	    url: "rutas/",
        	    method: "POST",
        	    body: nuevoDatos,
			}),
    	    invalidatesTags: ["Rutas"],
		}),
	putRutas: builder.mutation({ 
    		query: (datos) => ({
        		url: "rutas/",
        		method: "PUT",
        		body: datos,
			}),
    		invalidatesTags: ["Rutas"],
		}),
	getRoles: builder.query({ 
    		query: () => "roles/",
    		providesTags: ["Roles"],
		}),
	getRolesById: builder.query({
		query: (id) => `roles/${id}/`, // Ruta con el parámetro dinámico `id`
		providesTags: (result, error, id) => [{ type: "Roles", id }],
	}),
	postRolesByField: builder.mutation({
		query: (filter) => ({
			url: "roles/search/",
			method: "POST",
			body: filter, // Enviar el filtro como un objeto
		}),
		providesTags: (result, error, filter) => [{ type: "Roles", filter }],
		}),		
    postRoles: builder.mutation({ 
        	query: (nuevoDatos) => ({
        	    url: "roles/",
        	    method: "POST",
        	    body: nuevoDatos,
			}),
    	    invalidatesTags: ["Roles"],
		}),
	putRoles: builder.mutation({ 
    		query: (datos) => ({
        		url: "roles/",
        		method: "PUT",
        		body: datos,
			}),
    		invalidatesTags: ["Roles"],
		}),
	getUsuarios: builder.query({ 
    		query: () => "usuarios/",
    		providesTags: ["Usuarios"],
		}),
	getUsuariosById: builder.query({
		query: (id) => `usuarios/${id}/`, // Ruta con el parámetro dinámico `id`
		providesTags: (result, error, id) => [{ type: "Usuarios", id }],
	}),
	postUsuariosByField: builder.mutation({
		query: (filter) => ({
			url: "usuarios/search/",
			method: "POST",
			body: filter, // Enviar el filtro como un objeto
		}),
		providesTags: (result, error, filter) => [{ type: "Usuarios", filter }],
		}),		
    postUsuarios: builder.mutation({ 
        	query: (nuevoDatos) => ({
        	    url: "usuarios/",
        	    method: "POST",
        	    body: nuevoDatos,
			}),
    	    invalidatesTags: ["Usuarios"],
		}),
	putUsuarios: builder.mutation({ 
    		query: (datos) => ({
        		url: "usuarios/",
        		method: "PUT",
        		body: datos,
			}),
    		invalidatesTags: ["Usuarios"],
		}),
	patchUsuarios: builder.mutation({ 
		query: (datos) => ({
			url: "usuarios/",
			method: "PATCH",
			body: datos,
		}),
		invalidatesTags: ["Usuarios"],
	}),

    }),

});
export const {
	useGetMotivosQuery,
	usePostMotivosMutation,
	usePutMotivosMutation,
	usePatchMotivosMutation,
	usePostMotivosByFieldMutation,
	useGetDistinctMotivosQuery,
	useGetEscuelasQuery,
	usePostEscuelasMutation,
	usePutEscuelasMutation,
	usePatchEscuelasMutation,
	usePostEscuelasByFieldMutation,
	useGetDistinctEscuelasQuery,
	useGetPersonasQuery,
	usePostPersonasMutation,
	usePutPersonasMutation,
	usePatchPersonasMutation,
	usePostPersonasByFieldMutation,
	useGetDistinctPersonasQuery,
	usePostLoginByFieldMutation, 
	useGetRutasQuery,
	usePostRutasMutation,
	usePutRutasMutation,
	usePostRutasByFieldMutation,
	useGetRolesQuery,
	usePostRolesMutation,
	usePutRolesMutation,
	usePostRolesByFieldMutation,
	useGetUsuariosQuery,
	usePostUsuariosMutation,
	usePostUsuariosByFieldMutation,
	usePutUsuariosMutation,
	usePatchUsuariosMutation,
} = objetosApi;
