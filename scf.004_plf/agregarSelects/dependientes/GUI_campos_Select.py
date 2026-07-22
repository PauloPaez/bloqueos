#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox
import json

# Lista para almacenar los campos ingresados
arreglo_campos = []
# Opciones para el select de tipos de datos
tipos_dato = ["str", "int", "float", "file", "bool", "datetime", "select"]

def pluralizar(palabra):
    """Función para pluralizar palabras en español según reglas gramaticales."""
    vocales = {'a', 'e', 'i', 'o', 'u'}
    
    if not palabra:
        return palabra
    
    # Casos especiales
    if palabra.lower().endswith('z'):
        return palabra[:-1] + "ces"
    elif palabra.lower().endswith(('s', 'x')):
        return palabra + "es"
    elif palabra.lower().endswith('y') and len(palabra) > 1 and palabra[-2].lower() not in vocales:
        return palabra[:-1] + "ies"
    elif palabra.lower().endswith(('á', 'é', 'í', 'ó', 'ú')):
        return palabra + "s"
    elif palabra.lower().endswith('n') or palabra.lower().endswith('r'):
        return palabra + "es"
    else:
        return palabra + "s"

def agregar_campo():
    """Función para agregar un campo al arreglo."""
    nombre = entry_nombre.get().strip()
    tipo = tipo_var.get().strip()
    etiqueta = entry_etiqueta.get().strip()
    placeholder = entry_placeholder.get().strip()

    if not nombre or not tipo or not etiqueta:
        messagebox.showwarning("Advertencia", "Los campos Nombre, Tipo y Etiqueta son obligatorios.")
        return

    # Crear el diccionario del campo
    if tipo == "select":
        optionsKey = pluralizar(nombre)
        campo = {
            "name": nombre,
            "label": etiqueta,
            "type": tipo,
            "optionsKey": optionsKey
        }
        if placeholder:
            campo["placeholder"] = placeholder
    else:
        campo = {"name": nombre, "type": tipo, "label": etiqueta}
        if placeholder:
            campo["placeholder"] = placeholder

    arreglo_campos.append(campo)
    mensaje = (
        f"Nombre: {nombre}\n"
        f"Tipo: {tipo}\n"
        f"Etiqueta: {etiqueta}\n"
        f"Placeholder: {placeholder if placeholder else 'N/A'}"
    )
    if tipo == "select":
        mensaje += f"\nOptionsKey: {optionsKey}"
    messagebox.showinfo("Objeto agregado", mensaje)
    
    # Limpiar las entradas
    entry_nombre.delete(0, tk.END)
    tipo_var.set(tipos_dato[0])
    entry_etiqueta.delete(0, tk.END)
    entry_placeholder.delete(0, tk.END)

def guardar_archivo():
    """Función para guardar el arreglo en un archivo JSON."""
    if not arreglo_campos:
        messagebox.showwarning("Advertencia", "No hay campos para guardar.")
        return
    
    archivo = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        try:
            # Campos adicionales que se agregan automáticamente
            campo = {"name": "empresa", "type": "str", "label": "Empresa", "placeholder": "no_visible"}
            arreglo_campos.append(campo)
            campo = {"name": "activo", "type": "bool", "label": "Activo", "placeholder": "Activo"}
            arreglo_campos.append(campo)

            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(arreglo_campos, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("Éxito", "El archivo se guardó correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Generador de Arreglo de Campos")
ventana.geometry("400x400")

# Entradas de datos
tk.Label(ventana, text="Nombre del Campo:").pack(pady=5)
entry_nombre = tk.Entry(ventana, width=40)
entry_nombre.pack()

tk.Label(ventana, text="Tipo de Dato:").pack(pady=5)
tipo_var = tk.StringVar(ventana)
tipo_var.set(tipos_dato[0])
option_menu_tipo = tk.OptionMenu(ventana, tipo_var, *tipos_dato)
option_menu_tipo.pack()

tk.Label(ventana, text="Etiqueta:").pack(pady=5)
entry_etiqueta = tk.Entry(ventana, width=40)
entry_etiqueta.pack()

tk.Label(ventana, text="Placeholder (opcional):").pack(pady=5)
entry_placeholder = tk.Entry(ventana, width=40)
entry_placeholder.pack()

# Botones
boton_agregar = tk.Button(ventana, text="Ingresar otro", command=agregar_campo)
boton_agregar.pack(pady=10)

boton_guardar = tk.Button(ventana, text="Grabar", command=guardar_archivo)
boton_guardar.pack(pady=10)

# Iniciar la ventana
ventana.mainloop()
