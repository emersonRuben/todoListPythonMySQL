import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime


def agregar_tareas():
    modal = tk.Toplevel(ventana)
    modal.title("Agregar Tarea")
    modal.geometry("300x250")

    etiqueta_nombre = tk.Label(modal, text="Nombre de la Tarea:")
    etiqueta_nombre.pack(pady=5)
    entrada_nombre = tk.Entry(modal) 
    entrada_nombre.pack(pady=5)

    etiqueta_descripcion = tk.Label(modal, text="Descripción:")
    etiqueta_descripcion.pack(pady=5)
    entrada_descripcion = tk.Entry(modal)
    entrada_descripcion.pack(pady=5)

    etiqueta_fecha = tk.Label(modal, text="Fecha de Vencimiento:")
    etiqueta_fecha.pack(pady=5)
    entrada_fecha = DateEntry(modal, date_pattern="yyyy/mm/dd")
    entrada_fecha.pack(pady=5)

    def agregar_tarea():
        nombre_tarea = entrada_nombre.get()
        descripcion_tarea = entrada_descripcion.get()
        fecha_vencimiento = entrada_fecha.get()

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345",
                database="todoList"
            )
            
            with conexion.cursor(prepared=True) as cursor:
                consulta = "INSERT INTO tareas (titulo, descripcion, fecha_vencimiento, completada) VALUES (%s, %s, %s, %s)"
                valores = (nombre_tarea, descripcion_tarea, fecha_vencimiento, 0)
                cursor.execute(consulta, valores)
            conexion.commit()

            messagebox.showinfo("Tarea Agregada", "Tarea agregada con éxito")

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al agregar tarea: {error}")

        finally:
            if 'conexion' in locals():
                conexion.close()

        modal.destroy()  
        mostrar_tareas()
    
    boton_agregar_tarea = tk.Button(modal, text="Agregar Tarea", command=agregar_tarea)
    boton_agregar_tarea.pack(pady=10)
def marcar_completado(tarea_id, etiqueta_tarea):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="todoList"
        )
        
        with conexion.cursor(prepared=True) as cursor:
            consulta = "UPDATE tareas SET completada = 1 WHERE id = %s"
            valores = (tarea_id,)
            cursor.execute(consulta, valores)
        conexion.commit()

        messagebox.showinfo("Tarea completada", "Felicitaciones, has completado la tarea")

        etiqueta_tarea.config(font=("Arial", 12, "normal", "overstrike"))

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error al marcar tarea como completada: {error}")

    finally:
        if 'conexion' in locals():
            conexion.close()
def editar_tareas(tarea_id, etiqueta_tarea):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="todoList"
        )

        with conexion.cursor(prepared=True) as cursor:
            consulta = "SELECT titulo, descripcion, fecha_vencimiento, completada FROM tareas WHERE id = %s"
            valores = (tarea_id,)
            cursor.execute(consulta, valores)
            tarea = cursor.fetchone()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error al obtener detalles de la tarea: {error}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    if tarea[3] == 1:
        messagebox.showinfo("Tarea Completada", "Esta tarea ya está completada y no se puede editar.")
        return  

    def guardar_cambios():
        nuevo_titulo = entrada_nombre.get()
        nueva_descripcion = entrada_descripcion.get()
        nueva_fecha_vencimiento = entrada_fecha.get()

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345",
                database="todoList"
            )
            
            with conexion.cursor(prepared=True) as cursor:
                consulta = "UPDATE tareas SET titulo = %s, descripcion = %s, fecha_vencimiento = %s WHERE id = %s"
                valores = (nuevo_titulo, nueva_descripcion, nueva_fecha_vencimiento, tarea_id)
                cursor.execute(consulta, valores)
            conexion.commit()

            etiqueta_tarea.config(text=f"{nuevo_titulo} - {nueva_descripcion} - {nueva_fecha_vencimiento}")

            modal.destroy()

            messagebox.showinfo("Éxito", "Los cambios se guardaron correctamente.")

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al guardar cambios: {error}")

        finally:
            if 'conexion' in locals():
                conexion.close()

    modal = tk.Toplevel(ventana)
    modal.title("Editar Tarea")
    modal.geometry("300x250")

    etiqueta_nombre = tk.Label(modal, text="Nuevo Título:")
    etiqueta_nombre.pack(pady=5)
    entrada_nombre = tk.Entry(modal)
    entrada_nombre.insert(0, tarea[0])  
    entrada_nombre.pack(pady=5)

    etiqueta_descripcion = tk.Label(modal, text="Nueva Descripción:")
    etiqueta_descripcion.pack(pady=5)
    entrada_descripcion = tk.Entry(modal)
    entrada_descripcion.insert(0, tarea[1])
    entrada_descripcion.pack(pady=5)

    etiqueta_fecha = tk.Label(modal, text="Nueva Fecha de Vencimiento")
    etiqueta_fecha.pack(pady=5)
    entrada_fecha = DateEntry(modal, date_pattern="yyyy/mm/dd")
    entrada_fecha.delete(0, 'end')  
    entrada_fecha.insert(0, tarea[2]) 
    entrada_fecha.pack(pady=5)

    boton_guardar = tk.Button(modal, text="Guardar Cambios", command=guardar_cambios)
    boton_guardar.pack(pady=10)
def eliminar_tareas(tarea_id, marco_tarea, marco_botones):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="todoList"
        )
        
        with conexion.cursor(prepared=True) as cursor:
            consulta = "DELETE FROM tareas WHERE id=%s"
            valores = (tarea_id,)  
            cursor.execute(consulta, valores)
        conexion.commit()
        marco_tarea.destroy()
        marco_botones.destroy()

        messagebox.showinfo("Tarea Eliminada", "Tarea eliminada con éxito")

        mostrar_tareas()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error al eliminar tarea: {error}")

    finally:
        if 'conexion' in locals():
            conexion.close()
def mostrar_tareas():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="todoList"
        )

        with conexion.cursor(prepared=True) as cursor:
            consulta = "SELECT id, titulo, descripcion, fecha_vencimiento, completada FROM tareas"
            cursor.execute(consulta)
            tareas = cursor.fetchall()

            contY = 45
            for tarea in tareas:
                tarea_id, titulo, descripcion, fecha_vencimiento, completada = tarea
                marco_tarea = tk.Frame(ventana)
                marco_tarea.pack(pady=5)
                marco_tarea.place(x=100, y=55+contY)

                etiqueta_tarea = tk.Label(marco_tarea, text=f"{titulo} - {descripcion} - {fecha_vencimiento}")
                etiqueta_tarea.pack(side=tk.LEFT)

                marco_botones = tk.Frame(ventana)
                marco_botones.place(x=500, y=55+contY)

                boton_completado = tk.Button(marco_botones, text="Completado", command=lambda tarea_id=tarea_id, etiqueta_tarea=etiqueta_tarea: marcar_completado(tarea_id, etiqueta_tarea))
                boton_editar = tk.Button(marco_botones, text="Editar", command=lambda tarea_id=tarea_id, etiqueta_tarea=etiqueta_tarea: editar_tareas(tarea_id, etiqueta_tarea))
                boton_eliminar = tk.Button(marco_botones, text="Eliminar", command=lambda tarea_id=tarea_id, marco_tarea=marco_tarea, marco_botones=marco_botones: eliminar_tareas(tarea_id, marco_tarea, marco_botones))

                boton_completado.pack(side=tk.LEFT, padx=5)
                boton_editar.pack(side=tk.LEFT, padx=5)
                boton_eliminar.pack(side=tk.LEFT, padx=5)

                contY += 35
                if(completada==1):
                    etiqueta_tarea.config(font=("Arial", 12, "normal", "overstrike"))

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error al mostrar tareas: {error}")

    finally:
        if 'conexion' in locals():
            conexion.close()

ventana = tk.Tk()
ventana.title("TodoList")
ventana.geometry("500x400")

etiqueta = tk.Label(ventana, text="¡Bienvenido a tu Lista de Tareas!", font=("Arial", 20), bg="#D47138", fg="white")
etiqueta.pack(pady=10)  

etiqueta = tk.Label(ventana, text="Mis tareas:", font=("Arial", 15))
etiqueta.place(x=100, y=50)
mostrar_tareas()

boton_agregar = tk.Button(ventana, text="Agregar Tarea", font=("Arial", 15), command=agregar_tareas)
boton_agregar.place(x=300, y=50)

ventana.mainloop()
