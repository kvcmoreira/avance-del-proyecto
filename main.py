# main.py
from inventory import Inventario

def menu():
    inventario = Inventario()

    while True:
        print("\n" + "="*50)
        print("         SISTEMA DE GESTIÓN DE INVENTARIO")
        print("="*50)
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        print("="*50)

        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            try:
                id_prod = int(input("ID del producto: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                producto = Producto(id_prod, nombre, cantidad, precio)
                inventario.añadir_producto(producto)
            except ValueError as e:
                print(f"Entrada inválida: {e}")

        elif opcion == "2":
            try:
                id_prod = int(input("ID del producto a eliminar: "))
                inventario.eliminar_producto(id_prod)
            except ValueError:
                print("Por favor ingrese un número válido.")

        elif opcion == "3":
            try:
                id_prod = int(input("ID del producto a actualizar: "))
                nueva_cantidad = input("Nueva cantidad (deje vacío para no cambiar): ")
                nuevo_precio = input("Nuevo precio (deje vacío para no cambiar): ")

                cantidad = int(nueva_cantidad) if nueva_cantidad else None
                precio = float(nuevo_precio) if nuevo_precio else None

                inventario.actualizar_producto(id_prod, cantidad, precio)
            except ValueError:
                print("Entrada inválida.")

        elif opcion == "4":
            nombre = input("Ingrese parte del nombre del producto: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                print(f"\nResultados para '{nombre}':")
                for prod in resultados:
                    print(prod)
            else:
                print("No se encontraron productos con ese nombre.")

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("Gracias por usar el sistema de inventario.")
            inventario.cerrar_conexion()
            break

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()