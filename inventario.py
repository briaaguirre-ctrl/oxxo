from producto import Producto

class Inventario:

    def __init__(self):
        self.__productos = {}

    def agregar_producto(self, producto):

        codigo = producto.codigo

        if codigo in self.__productos:
            raise ValueError("Ya existe un producto con ese código.")

        self.__productos[codigo] = producto

    def buscar_producto(self, codigo):

        producto = self.__productos.get(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        return producto

    def modificar_producto(self, codigo, nombre, categoria, precio):

        producto = self.buscar_producto(codigo)

        producto.modificar(nombre, categoria, precio)

    def modificar_stock(self, codigo, nuevo_stock):

        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        producto = self.buscar_producto(codigo)

        diferencia = nuevo_stock - producto.stock

        if diferencia > 0:
            producto.agregar_stock(diferencia)

        elif diferencia < 0:
            producto.reducir_stock(-diferencia)

    def eliminar_producto(self, codigo):

        producto = self.buscar_producto(codigo)

        del self.__productos[codigo]

        return producto

    def listar_productos(self):

        return list(self.__productos.values())

    def cantidad_productos(self):

        return len(self.__productos)
