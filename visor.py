import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class VisorArchivos:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de archivos CSV y Excel")
        self.root.geometry("1000x600")

        # Frame superior: selección de carpeta
        frame_carpeta = ttk.Frame(self.root, padding=5)
        frame_carpeta.pack(fill=tk.X)

        ttk.Label(frame_carpeta, text="Carpeta:").pack(side=tk.LEFT)
        self.ruta_carpeta = tk.StringVar()
        ttk.Entry(frame_carpeta, textvariable=self.ruta_carpeta, width=60).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_carpeta, text="Examinar...", command=self.seleccionar_carpeta).pack(side=tk.LEFT)

        # Frame medio: lista de archivos
        frame_lista = ttk.Frame(self.root, padding=5)
        frame_lista.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ttk.Label(frame_lista, text="Archivos disponibles:").pack(anchor=tk.W)
        self.lista_archivos = tk.Listbox(frame_lista, width=40, height=25)
        self.lista_archivos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_lista = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.lista_archivos.yview)
        scroll_lista.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_archivos.config(yscrollcommand=scroll_lista.set)

        # Botón para visualizar
        ttk.Button(frame_lista, text="Visualizar seleccionado", command=self.visualizar_archivo).pack(pady=5)

        # Frame derecho: visualización de datos
        frame_tabla = ttk.Frame(self.root, padding=5)
        frame_tabla.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(frame_tabla, text="Vista previa del archivo:").pack(anchor=tk.W)

        # Contenedor para Treeview + scrollbars
        contenedor_tabla = ttk.Frame(frame_tabla)
        contenedor_tabla.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(contenedor_tabla)
        scroll_y = ttk.Scrollbar(contenedor_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(contenedor_tabla, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
        contenedor_tabla.grid_rowconfigure(0, weight=1)
        contenedor_tabla.grid_columnconfigure(0, weight=1)

    def seleccionar_carpeta(self):
        """Abre diálogo para elegir carpeta y lista los archivos válidos"""
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta con archivos CSV/Excel")
        if carpeta:
            self.ruta_carpeta.set(carpeta)
            self.actualizar_lista_archivos()

    def actualizar_lista_archivos(self):
        """Actualiza la lista de archivos .csv, .xlsx, .xls en la carpeta seleccionada"""
        self.lista_archivos.delete(0, tk.END)
        carpeta = self.ruta_carpeta.get()
        if not os.path.isdir(carpeta):
            return

        extensiones = ('.csv', '.xlsx', '.xls')
        for archivo in os.listdir(carpeta):
            if archivo.lower().endswith(extensiones):
                self.lista_archivos.insert(tk.END, archivo)

        if self.lista_archivos.size() == 0:
            messagebox.showinfo("Sin archivos", "No se encontraron archivos CSV o Excel en la carpeta seleccionada.")

    def visualizar_archivo(self):
        """Lee el archivo seleccionado y lo muestra en la tabla"""
        seleccion = self.lista_archivos.curselection()
        if not seleccion:
            messagebox.showwarning("Selección vacía", "Por favor, selecciona un archivo de la lista.")
            return

        archivo = self.lista_archivos.get(seleccion[0])
        ruta_completa = os.path.join(self.ruta_carpeta.get(), archivo)

        try:
            # Leer según extensión
            ext = os.path.splitext(archivo)[1].lower()
            if ext == '.csv':
                df = pd.read_csv(ruta_completa)
            elif ext in ('.xlsx', '.xls'):
                df = pd.read_excel(ruta_completa)
            else:
                messagebox.showerror("Error", "Formato no soportado")
                return

            # Limpiar tabla anterior
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Configurar columnas
            columnas = list(df.columns)
            self.tree["columns"] = columnas
            self.tree["show"] = "headings"

            for col in columnas:
                self.tree.heading(col, text=col)
                # Ancho inicial aproximado
                self.tree.column(col, width=120, minwidth=60)

            # Insertar datos
            for _, fila in df.iterrows():
                valores = [str(v) for v in fila.values]
                self.tree.insert("", tk.END, values=valores)

            # Mostrar información adicional
            messagebox.showinfo("Cargado", f"Archivo '{archivo}' cargado correctamente.\nFilas: {df.shape[0]}, Columnas: {df.shape[1]}")

        except Exception as e:
            messagebox.showerror("Error al leer", f"No se pudo leer el archivo:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisorArchivos(root)
    root.mainloop()