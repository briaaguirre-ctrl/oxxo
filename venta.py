class Venta:

    def __init__(self, inventario):
        self.__inventario = inventario
        self.__productos = {}
        self.__confirmada = False

    def agregar_producto(self, codigo, cantidad):
        if self.__confirmada:
            raise ValueError("La venta ya fue confirmada.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        producto = self.__inventario.buscar_producto(codigo)

        cantidad_actual = self.__productos.get(codigo, 0)
        cantidad_total = cantidad_actual + cantidad

        if cantidad_total > producto.stock:
            raise ValueError("No hay suficiente stock disponible.")

        self.__productos[codigo] = cantidad_total

    def calcular_total(self):
        total = 0

        for codigo, cantidad in self.__productos.items():
            producto = self.__inventario.buscar_producto(codigo)
            total += producto.calcular_precio_final() * cantidad

        return total

    def listar_productos(self):
        detalle = []

        for codigo, cantidad in self.__productos.items():
            producto = self.__inventario.buscar_producto(codigo)

            detalle.append({
                "codigo": codigo,
                "nombre": producto.nombre,
                "cantidad": cantidad,
                "precio": producto.precio,
                "subtotal": producto.precio * cantidad
            })

        return detalle

    def confirmar_venta(self, metodo_pago, monto_recibido=0):
        if self.__confirmada:
            raise ValueError("Esta venta ya fue confirmada.")

        if not self.__productos:
            raise ValueError("No hay productos en la venta.")

        total = self.calcular_total()

        metodo_pago = metodo_pago.lower()

        if metodo_pago not in ["efectivo", "debito", "credito"]:
            raise ValueError("Método de pago no válido.")

        if metodo_pago == "efectivo":
            if monto_recibido < total:
                raise ValueError("El dinero recibido no alcanza para pagar.")

            vuelto = monto_recibido - total
        else:
            vuelto = 0

        for codigo, cantidad in self.__productos.items():
            producto = self.__inventario.buscar_producto(codigo)

            if cantidad > producto.stock:
                raise ValueError(
                    f"Stock insuficiente para {producto.nombre}."
                )

        for codigo, cantidad in self.__productos.items():
            producto = self.__inventario.buscar_producto(codigo)
            producto.reducir_stock(cantidad)

        self.__confirmada = True

        return {
            "total": total,
            "metodo_pago": metodo_pago,
            "vuelto": vuelto
        }
