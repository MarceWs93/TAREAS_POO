import json


# Clase que representa un producto en el inventario
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Métodos para obtener los atributos del producto
    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio


# Clase que representa el inventario de productos
class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario para almacenar los productos

    # Añadir un nuevo prodcuto
    def añadir_producto(self, producto):
        self.productos[producto.get_id()] = producto
        print(f"Producto {producto.get_nombre()} añadido.")

    # Eliminar el producto del inventario
    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            print(f"Producto con ID {id_producto} eliminado.")
        else:
            print("! Error: Producto no encontrado.")

    # Actualizar los productos
    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto in self.productos:
            producto = self.productos[id_producto]
            if cantidad is not None:
                producto.cantidad = cantidad
            if precio is not None:
                producto.precio = precio
            print(f"Producto con ID {id_producto} actualizado.")
        else:
            print("! Error: Producto no encontrado.")

    # Buscar los productos
    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]
        return resultados

    # Mostrar los prodcutos
    def mostrar_productos(self):
        if len(self.productos) == 0:
            print("No hay productos en el inventario.")
        else:
            print("\nLista de productos:")
            print("-" * 60)
            print(f"{'ID':<10} {'Nombre':<20} {'Cantidad':<10} {'Precio ($)':<10}")
            print("-" * 60)
            for p in self.productos.values():
                print(f"{p.get_id():<10} {p.get_nombre():<20} {p.get_cantidad():<10} {p.get_precio():<10.2f}")
            print("-" * 60)

    # Guarda los productos en el archi json
    def guardar_productos(self, filename="productos.json"):
        with open(filename, "w") as file:
            json.dump({id: p.__dict__ for id, p in self.productos.items()}, file)
        print("Productos guardados en archivo.")

    #metodo para el archivo json
    def cargar_productos(self, filename="productos.json"):
        try:
            with open(filename, "r") as file:
                productos_dict = json.load(file)
                self.productos = {id: Producto(**data) for id, data in productos_dict.items()}
            print("Productos cargados desde archivo.")
        except FileNotFoundError:
            print("! Error: Archivo no encontrado.")


# Función para mostrar el menú y gestionar las opciones del usuario
def menu():
    inventario = Inventario()
    inventario.cargar_productos()  # Cargar productos al iniciar
    while True:
        print("\nMenú de Gestión de Inventarios")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        try:
            opcion = input("\nSeleccione una opción: ")

            if opcion == '1':
                print("\nAñadir nuevo producto")
                id_producto = input("ID del producto: ")
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: $"))
                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.añadir_producto(producto)

            elif opcion == '2':
                print("\nEliminar producto")
                id_producto = input("ID del producto a eliminar: ")
                inventario.eliminar_producto(id_producto)

            elif opcion == '3':
                print("\nActualizar producto")
                id_producto = input("ID del producto a actualizar: ")
                try:
                    cantidad = input("Nueva cantidad (Enter para mantener): ")
                    precio = input("Nuevo precio (Enter para mantener): ")
                    cantidad = int(cantidad) if cantidad.strip() else None
                    precio = float(precio) if precio.strip() else None
                    inventario.actualizar_producto(id_producto, cantidad, precio)
                except ValueError:
                    print("! Error: Los valores deben ser numéricos")

            elif opcion == '4':
                print("\nBuscar producto")
                nombre = input("Nombre a buscar: ")
                resultados = inventario.buscar_producto(nombre)
                if resultados:
                    print("\nProductos encontrados:")
                    print("-" * 60)
                    print(f"{'ID':<10} {'Nombre':<20} {'Cantidad':<10} {'Precio ($)':<10}")
                    print("-" * 60)
                    for p in resultados:
                        print(f"{p.get_id():<10} {p.get_nombre():<20} {p.get_cantidad():<10} {p.get_precio():<10.2f}")
                    print("-" * 60)
                else:
                    print("! No se encontraron productos")

            elif opcion == '5':
                inventario.mostrar_productos()

            elif opcion == '6':
                print("\n¡Hasta luego!")
                inventario.guardar_productos()  # Aseguramos que se guarden los cambios al salir
                break

            else:
                print("\n! Opción no válida")

        except ValueError:
            print("! Error: Ingrese valores válidos")
        except Exception as e:
            print(f"! Error: {str(e)}")


if __name__ == "__main__":
    menu()