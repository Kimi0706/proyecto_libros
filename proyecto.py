import csv
import os
import customtkinter as ctk
from tkinter import ttk  # Importamos ttk para usar la Tabla (Treeview)

# Configuración del tema visual
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class BiblioManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DE LA VENTANA ---
        self.title("BiblioManager Pro - Sistema de Gestión")
        self.geometry("600x650")
        self.resizable(False, False)
        self.archivo_csv = 'libros.csv'

        # --- ENCABEZADO ---
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(pady=(15, 5))

        self.lbl_titulo = ctk.CTkLabel(self.frame_header, text="📚 BiblioManager Pro", font=ctk.CTkFont(family="Arial", size=26, weight="bold"))
        self.lbl_titulo.pack()
        
        # --- SISTEMA DE PESTAÑAS (TABVIEW) ---
        self.tabview = ctk.CTkTabview(self, width=540, height=520)
        self.tabview.pack(pady=5, padx=20, fill="both", expand=True)

        # Creamos las dos pestañas
        self.tab_registro = self.tabview.add("Registrar Nuevo Libro")
        self.tab_inventario = self.tabview.add("Inventario de Libros")

        # Configurar la acción al cambiar de pestaña para recargar la tabla
        self.tabview.configure(command=self.al_cambiar_pestana)

        # ==========================================
        # PESTAÑA 1: FORMULARIO DE REGISTRO
        # ==========================================
        self.frame_form = ctk.CTkFrame(self.tab_registro, corner_radius=10)
        self.frame_form.pack(pady=10, padx=20, fill="both", expand=True)

        self.txt_codigo = self.crear_campo("Código del Libro (ISBN único):", self.frame_form)
        self.txt_titulo = self.crear_campo("Título del Libro:", self.frame_form)
        self.txt_autor = self.crear_campo("Autor principal:", self.frame_form)
        self.txt_anio = self.crear_campo("Año de Publicación:", self.frame_form)

        # Select de Categoría
        lbl_cat = ctk.CTkLabel(self.frame_form, text="Categoría:", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_cat.pack(anchor="w", padx=30, pady=(8, 2))
        
        categorias = ["Ficción", "No Ficción", "Ciencia Ficción", "Historia", "Tecnología", "Fantasía", "Biografía"]
        self.cmb_categoria = ctk.CTkComboBox(self.frame_form, values=categorias, width=440, state="readonly")
        self.cmb_categoria.pack(padx=30, pady=(0, 10))
        self.cmb_categoria.set("Ficción")

        # Botones y Estado (Ahora dentro de la pestaña de registro)
        self.btn_guardar = ctk.CTkButton(self.tab_registro, text="💾 Guardar Libro", font=("Arial", 14, "bold"), height=40, width=160, command=self.guardar_libro)
        self.btn_guardar.pack(pady=(15, 5))

        self.lbl_estado = ctk.CTkLabel(self.tab_registro, text="", font=ctk.CTkFont(size=13))
        self.lbl_estado.pack()

        # ==========================================
        # PESTAÑA 2: TABLA DE INVENTARIO
        # ==========================================
        self.lbl_inv_titulo = ctk.CTkLabel(self.tab_inventario, text="Inventario Actualizado", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_inv_titulo.pack(pady=(10, 5))

        # Estilo para que la tabla (Treeview) combine con el modo oscuro
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b")
        style.map('Treeview', background=[('selected', '#1f538d')])

        # Creación de la Tabla
        columnas = ("codigo", "titulo", "autor", "anio", "categoria")
        self.tabla = ttk.Treeview(self.tab_inventario, columns=columnas, show="headings", height=15)
        
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("titulo", text="Título")
        self.tabla.heading("autor", text="Autor")
        self.tabla.heading("anio", text="Año")
        self.tabla.heading("categoria", text="Categoría")

        # Tamaños de columnas
        self.tabla.column("codigo", width=80)
        self.tabla.column("titulo", width=180)
        self.tabla.column("autor", width=120)
        self.tabla.column("anio", width=50, anchor="center")
        self.tabla.column("categoria", width=90)

        self.tabla.pack(pady=5, padx=10, fill="both", expand=True)

        self.btn_recargar = ctk.CTkButton(self.tab_inventario, text="🔄 Recargar Datos", command=self.cargar_datos_tabla)
        self.btn_recargar.pack(pady=10)

    # --- FUNCIONES ---
    def crear_campo(self, texto_label, contenedor):
        lbl = ctk.CTkLabel(contenedor, text=texto_label, font=ctk.CTkFont(size=12, weight="bold"))
        lbl.pack(anchor="w", padx=30, pady=(8, 2))
        entrada = ctk.CTkEntry(contenedor, width=440)
        entrada.pack(padx=30, pady=(0, 0))
        return entrada

    def codigo_existe(self, codigo_buscar):
        """Función Anti-Duplicados: Lee el CSV y busca si el código ya existe"""
        if not os.path.isfile(self.archivo_csv):
            return False # Si no hay archivo, obvio no existe
        
        try:
            with open(self.archivo_csv, mode='r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                for fila in lector:
                    if fila and fila[0] == codigo_buscar:
                        return True # Se encontró el código!
            return False
        except Exception:
            return False

    def guardar_libro(self):
        codigo = self.txt_codigo.get().strip()
        titulo = self.txt_titulo.get().strip()
        autor = self.txt_autor.get().strip()
        anio = self.txt_anio.get().strip()
        categoria = self.cmb_categoria.get()

        if not (codigo and titulo and autor and anio):
            self.mostrar_mensaje("⚠️ Llena todos los campos.", "#FF5555")
            return

        # VALIDACIÓN ANTI-DUPLICADOS
        if self.codigo_existe(codigo):
            self.mostrar_mensaje(f"⛔ Error: El código '{codigo}' YA EXISTE en la base de datos.", "#FF5555")
            return

        encabezados = ['Código', 'Título', 'Autor', 'Año', 'Categoría']
        archivo_existe = os.path.isfile(self.archivo_csv)

        try:
            with open(self.archivo_csv, mode='a', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                if not archivo_existe:
                    escritor.writerow(encabezados)
                escritor.writerow([codigo, titulo, autor, anio, categoria])

            self.mostrar_mensaje(f"✅ ¡'{titulo}' registrado con éxito!", "#2ECC71")
            self.limpiar_formulario()
            
        except Exception as e:
            self.mostrar_mensaje(f"❌ Error al guardar: {e}", "#FF5555")

    def mostrar_mensaje(self, mensaje, color):
        self.lbl_estado.configure(text=mensaje, text_color=color)
        self.after(4000, lambda: self.lbl_estado.configure(text=""))

    def limpiar_formulario(self):
        self.txt_codigo.delete(0, 'end')
        self.txt_titulo.delete(0, 'end')
        self.txt_autor.delete(0, 'end')
        self.txt_anio.delete(0, 'end')
        self.cmb_categoria.set("Ficción")
        self.txt_codigo.focus()

    def al_cambiar_pestana(self):
        """Si el usuario hace clic en la pestaña de inventario, cargamos los datos"""
        if self.tabview.get() == "Inventario de Libros":
            self.cargar_datos_tabla()

    def cargar_datos_tabla(self):
        """Lee el CSV y lo mete en la tabla"""
        # Limpiar la tabla primero para no duplicar la vista
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if not os.path.isfile(self.archivo_csv):
            return

        try:
            with open(self.archivo_csv, mode='r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                encabezados = next(lector, None) # Saltamos la primera fila (títulos)
                for fila in lector:
                    if fila:
                        self.tabla.insert("", "end", values=fila)
        except Exception as e:
            print("Error al leer datos:", e)

if __name__ == "__main__":
    app = BiblioManagerApp()
    app.mainloop()
