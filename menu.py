import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from inventario import Inventario
from producto import Producto
from venta import Venta


class SistemaOXXO:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema OXXO")
        self.ventana.geometry("950x600")

        self.inventario = Inventario()
        self.venta = Venta(self.inventario)

        self.crear_interfaz()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana,
            text="SISTEMA OXXO",
            font=("Arial", 22, "bold"),
            fg="red"
        )
        titulo.pack(pady=10)

        pestañas = ttk.Notebook(self.ventana)
        pestañas.pack(fill="both", expand=True, padx=10, pady=10)

        self.pestaña_inventario = ttk.Frame(pestañas)
        self.pestaña_ventas = ttk.Frame(pestañas)

        pestañas.add(self.pestaña_inventario, text="Inventario")
        pestañas.add(self.pestaña_ventas, text="Ventas")

        self.crear_pestaña_inventario()
        self.crear_pestaña_ventas()


    def crear_pestaña_inventario(self):
        tk.Label(
            self.pestaña_inventario,
            text="Productos disponibles",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")

        self.tabla_inventario = ttk.Treeview(
            self.pestaña_inventario,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "codigo": "Código",
            "nombre": "Nombre",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock"
        }

        for columna in columnas:
            self.tabla_inventario.heading(
                columna, text=encabezados[columna]
            )

        self.tabla_inventario.pack(fill="both", expand=True, padx=10)

        botones = tk.Frame(self.pestaña_inventario)
        botones.pack(pady=15)

        tk.Button(
            botones, text="Agregar producto",
            command=self.agregar_producto
        ).pack(side="left", padx=5)

        tk.Button(
            botones, text="Modificar producto",
            command=self.modificar_producto
        ).pack(side="left", padx=5)

        tk.Button(
            botones, text="Modificar stock",
            command=self.modificar_stock
        ).pack(side="left", padx=5)

        tk.Button(
            botones, text="Eliminar producto",
            command=self.eliminar_producto
        ).pack(side="left", padx=5)

        self.actualizar_inventario()

    def actualizar_inventario(self):
        for fila in self.tabla_inventario.get_children():
            self.tabla_inventario.delete(fila)

        for producto in self.inventario.listar_productos():
            self.tabla_inventario.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:,}",
                    producto.stock
                )
            )
            
    def actualizar_productos_venta(self):
        for fila in self.tabla_productos_venta.get_children():
            self.tabla_productos_venta.delete(fila)

        for producto in self.inventario.listar_productos():
            self.tabla_productos_venta.insert(
                "",
                "end",
                values=(
                    producto.nombre,
                    f"${producto.precio:,}"
                )
            )
    
    def filtrar_productos_venta(self, evento=None):
        busqueda = self.buscar_venta.get().lower()

        for fila in self.tabla_productos_venta.get_children():
            self.tabla_productos_venta.delete(fila)

        for producto in self.inventario.listar_productos():
            if busqueda in producto.nombre.lower():
                self.tabla_productos_venta.insert(
                    "",
                    "end",
                    values=(
                        producto.nombre,
                        f"${producto.precio:,}"
                    )
                )
            
    def producto_seleccionado(self):
        seleccion = self.tabla_inventario.selection()

        if not seleccion:
            messagebox.showwarning(
                "Atención", "Selecciona un producto primero."
            )
            return None

        datos = self.tabla_inventario.item(seleccion[0], "values")
        return datos[0]

    def agregar_producto(self):
        codigo = simpledialog.askstring("Producto", "Código:")
        if codigo is None:
            return

        nombre = simpledialog.askstring("Producto", "Nombre:")
        if nombre is None:
            return

        categoria = simpledialog.askstring("Producto", "Categoría:")
        if categoria is None:
            return

        precio = simpledialog.askinteger(
            "Producto", "Precio en pesos chilenos:"
        )
        if precio is None:
            return

        stock = simpledialog.askinteger("Producto", "Stock inicial:")
        if stock is None:
            return

        try:
            producto = Producto(
                codigo, nombre, categoria, precio, stock
            )
            self.inventario.agregar_producto(producto)
            self.actualizar_inventario()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def modificar_producto(self):
        codigo = self.producto_seleccionado()
        if codigo is None:
            return

        nombre = simpledialog.askstring("Modificar", "Nuevo nombre:")
        if nombre is None:
            return

        categoria = simpledialog.askstring(
            "Modificar", "Nueva categoría:"
        )
        if categoria is None:
            return

        precio = simpledialog.askinteger(
            "Modificar", "Nuevo precio:"
        )
        if precio is None:
            return

        try:
            self.inventario.modificar_producto(
                codigo, nombre, categoria, precio
            )
            self.actualizar_inventario()
            messagebox.showinfo("Éxito", "Producto modificado.")

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def modificar_stock(self):
        codigo = self.producto_seleccionado()
        if codigo is None:
            return

        nuevo_stock = simpledialog.askinteger(
            "Stock", "Ingresa el nuevo stock:"
        )

        if nuevo_stock is None:
            return

        try:
            self.inventario.modificar_stock(codigo, nuevo_stock)
            self.actualizar_inventario()
            messagebox.showinfo("Éxito", "Stock actualizado.")

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def eliminar_producto(self):
        codigo = self.producto_seleccionado()
        if codigo is None:
            return

        confirmar = messagebox.askyesno(
            "Eliminar", "¿Estás seguro de eliminar este producto?"
        )

        if confirmar:
            self.inventario.eliminar_producto(codigo)
            self.actualizar_inventario()
            messagebox.showinfo("Éxito", "Producto eliminado.")


    def crear_pestaña_ventas(self):
        
        tk.Label(
            self.pestaña_ventas,
            text="Realizar una venta",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        tk.Label(
            self.pestaña_ventas,
            text="Buscar producto:"
            ).pack(pady=5)
        
        self.buscar_venta = tk.Entry(
            self.pestaña_ventas,
            width=35
            )
        self.buscar_venta.pack(pady=5)
        self.buscar_venta.bind("<KeyRelease>", self.filtrar_productos_venta)
        columnas_productos = ("nombre", "precio")

        self.tabla_productos_venta = ttk.Treeview(
            self.pestaña_ventas,
            columns=columnas_productos,
            show="headings",
            height=6
        )
        self.tabla_productos_venta.heading("nombre", text="Producto")
        self.tabla_productos_venta.heading("precio", text="Precio")

        self.tabla_productos_venta.pack(
            fill="x", padx=10, pady=10
        )
        self.actualizar_productos_venta()

        ttk.Button(
            self.pestaña_ventas,
            text="Agregar producto seleccionado",
            command=self.agregar_a_venta
        ).pack(pady=5)

        columnas = ("codigo", "nombre", "cantidad", "subtotal")

        self.tabla_venta = ttk.Treeview(
            self.pestaña_ventas,
            columns=columnas,
            show="headings",
            height=8
        )

        for columna in columnas:
            self.tabla_venta.heading(
                columna, text=columna.capitalize()
            )

        self.tabla_venta.pack(fill="both", expand=True, padx=10, pady=10)

        self.etiqueta_total = tk.Label(
            self.pestaña_ventas,
            text="Total: $0",
            font=("Arial", 16, "bold")
        )
        self.etiqueta_total.pack(pady=5)

        zona_pago = tk.Frame(self.pestaña_ventas)
        zona_pago.pack(pady=10)

        tk.Label(zona_pago, text="Método de pago:").grid(
            row=0, column=0, padx=5
        )

        self.metodo_pago = ttk.Combobox(
            zona_pago,
            values=["Efectivo", "Debito", "Credito"],
            state="readonly",
            width=15
        )
        self.metodo_pago.set("Efectivo")
        self.metodo_pago.grid(row=0, column=1, padx=5)

        tk.Label(zona_pago, text="Dinero recibido:").grid(
            row=0, column=2, padx=5
        )

        self.entrada_efectivo = tk.Entry(zona_pago, width=15)
        self.entrada_efectivo.grid(row=0, column=3, padx=5)

        tk.Button(
            self.pestaña_ventas,
            text="CONFIRMAR VENTA",
            command=self.confirmar_venta,
            bg="red",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(pady=10)
        
    def agregar_a_venta(self):
        seleccion = self.tabla_productos_venta.selection()

        if not seleccion:
            messagebox.showwarning(
                "Atención", "Selecciona un producto primero."
            )
            return

        nombre = self.tabla_productos_venta.item(
            seleccion[0], "values"
        )[0]

        codigo = None

        for producto in self.inventario.listar_productos():
            if producto.nombre == nombre:
                codigo = producto.codigo
                break

        if codigo is None:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        cantidad = simpledialog.askinteger(
            "Cantidad", "¿Cuántas unidades deseas vender?"
        )

        if cantidad is None:
            return

        try:
            self.venta.agregar_producto(codigo, cantidad)
            self.actualizar_tabla_venta()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def actualizar_tabla_venta(self):
        for fila in self.tabla_venta.get_children():
            self.tabla_venta.delete(fila)

        for producto in self.venta.listar_productos():
            self.tabla_venta.insert(
                "",
                "end",
                values=(
                    producto["codigo"],
                    producto["nombre"],
                    producto["cantidad"],
                    f"${producto['subtotal']:,}"
                )
            )

        total = self.venta.calcular_total()
        self.etiqueta_total.config(text=f"Total: ${total:,}")
        self.ventana.update_idletasks()

    def confirmar_venta(self):
        metodo = self.metodo_pago.get().lower()
        monto = 0

        if metodo == "efectivo":
            try:
                monto = int(self.entrada_efectivo.get())
            except ValueError:
                messagebox.showerror(
                    "Error", "Ingresa un monto recibido válido."
                )
                return

        try:
            resultado = self.venta.confirmar_venta(metodo, monto)

            mensaje = (
                f"Venta realizada correctamente.\n"
                f"Total: ${resultado['total']:,}\n"
                f"Método de pago: {resultado['metodo_pago'].capitalize()}\n"
                f"Vuelto: ${resultado['vuelto']:,}"
            )

            messagebox.showinfo("Venta confirmada", mensaje)

            self.venta = Venta(self.inventario)
            self.entrada_efectivo.delete(0, tk.END)
            self.actualizar_tabla_venta()
            self.actualizar_inventario()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

ventana = tk.Tk()
aplicacion = SistemaOXXO(ventana)
ventana.mainloop()
