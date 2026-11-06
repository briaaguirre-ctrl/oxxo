
from vendible import Vendible


class Producto(Vendible):

    def __init__(self, codigo, nombre, categoria, precio, stock):

        self.__codigo = codigo
        self.__nombre = nombre
        self.__categoria = categoria
        self.__precio = precio
        self.__stock = stock


    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def categoria(self):
        return self.__categoria

    @property
    def precio(self):
        return self.__precio

    @property
    def stock(self):
        return self.__stock


    def modificar(self, nombre, categoria, precio):

        if nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero")

        self.__nombre = nombre
        self.__categoria = categoria
        self.__precio = precio

   

    def agregar_stock(self, cantidad):

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

        self.__stock += cantidad


    def reducir_stock(self, cantidad):

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

        if cantidad > self.__stock:
            raise ValueError("No hay suficiente inventario")

        self.__stock -= cantidad

    # Calcular precio de venta

    def calcular_precio_final(self):
        return self.__precio

    def __str__(self):

        return (
            f"{self.__codigo} - {self.__nombre} | "
            f"{self.__categoria} | "
            f"${self.__precio:,} | "
            f"Stock: {self.__stock}"
        )

