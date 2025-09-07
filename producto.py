# producto.py
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    def set_cantidad(self, cantidad):
        if cantidad >= 0:
            self.cantidad = cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")

    def set_precio(self, precio):
        if precio >= 0:
            self.precio = precio
        else:
            raise ValueError("El precio no puede ser negativo")

    def __str__(self):
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"