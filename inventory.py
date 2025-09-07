# inventory.py
from producto import Producto
import sqlite3
from typing import Dict, List, Optional

class Inventario:
    def __init__(self, db_path="inventario.db"):
        self.db_path = db_path
        self.productos: Dict[int, Producto] = {}
        self.conectar_db()
        self.cargar_productos()

    def conectar_db(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.crear_tabla()
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")

    def crear_tabla(self):
        query = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def cargar_productos(self):
        try:
            self.cursor.execute("SELECT id, nombre, cantidad, precio FROM productos")
            rows = self.cursor.fetchall()
            for row in rows:
                producto = Producto(row[0], row[1], row[2], row[3])
                self.productos[row[0]] = producto
        except Exception as e:
            print(f"Error al cargar productos: {e}")

    def guardar_en_db(self, producto: Producto):
        try:
            if producto.get_id() in self.productos:
                self.cursor.execute(
                    "UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?",
                    (producto.get_nombre(), producto.get_cantidad(), producto.get_precio(), producto.get_id())
                )
            else:
                self.cursor.execute(
                    "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                    (producto.get_nombre(), producto.get_cantidad(), producto.get_precio())
                )
            self.conn.commit()
        except Exception as e:
            print(f"Error al guardar en base de datos: {e}")

    def añadir_producto(self, producto: Producto):
        if producto.get_id() in self.productos:
            print(f"Error: Ya existe un producto con ID {producto.get_id()}")
            return False
        self.productos[producto.get_id()] = producto
        self.guardar_en_db(producto)
        print(f"Producto '{producto.get_nombre()}' añadido exitosamente.")
        return True

    def eliminar_producto(self, id_producto: int):
        if id_producto not in self.productos:
            print(f"No se encontró un producto con ID {id_producto}")
            return False
        nombre = self.productos[id_producto].get_nombre()
        del self.productos[id_producto]
        self.cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        self.conn.commit()
        print(f"Producto '{nombre}' eliminado correctamente.")
        return True

    def actualizar_producto(self, id_producto: int, nueva_cantidad=None, nuevo_precio=None):
        if id_producto not in self.productos:
            print(f"No se encontró un producto con ID {id_producto}")
            return False

        producto = self.productos[id_producto]

        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)
        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)

        self.guardar_en_db(producto)
        print(f"Producto '{producto.get_nombre()}' actualizado.")
        return True

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        resultados = []
        for producto in self.productos.values():
            if nombre.lower() in producto.get_nombre().lower():
                resultados.append(producto)
        return resultados

    def mostrar_todos(self):
        if not self.productos:
            print("No hay productos en el inventario.")
            return
        print("\n=== LISTA DE TODOS LOS PRODUCTOS ===")
        for producto in self.productos.values():
            print(producto)

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()