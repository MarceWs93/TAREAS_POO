# Definición de la clase Libro
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        # Almacenamos título y autor como tupla ya que son inmutables
        self.info = (titulo, autor)  # Tupla con información inmutable
        self.categoria = categoria  # Categoría del libro
        self.isbn = isbn  # ISBN como identificador único
        self.disponible = True  # Estado de disponibilidad del libro

    @property
    def titulo(self):
        # Getter para acceder al título desde la tupla
        return self.info[0]

    @property
    def autor(self):
        # Getter para acceder al autor desde la tupla
        return self.info[1]

    def __str__(self):
        # Representación en string del libro
        estado = "Disponible" if self.disponible else "Prestado"
        return f"Libro: {self.titulo} | Autor: {self.autor} | Categoría: {self.categoria} | ISBN: {self.isbn} | Estado: {estado}"


# Definición de la clase Usuario
class Usuario:
    def __init__(self, nombre, usuario_id):
        self.nombre = nombre  # Nombre del usuario
        self.usuario_id = usuario_id  # ID único del usuario
        self.libros_prestados = []  # Lista para almacenar libros prestados

    def prestar_libro(self, libro):
        # Añade un libro a la lista de préstamos del usuario
        self.libros_prestados.append(libro)

    def devolver_libro(self, isbn):
        # Devuelve un libro basado en su ISBN
        for i, libro in enumerate(self.libros_prestados):
            if libro.isbn == isbn:
                # Eliminamos el libro de la lista de préstamos
                return self.libros_prestados.pop(i)
        return None  # Si no se encuentra el libro

    def listar_libros_prestados(self):
        # Muestra todos los libros prestados al usuario
        if not self.libros_prestados:
            return f"El usuario {self.nombre} no tiene libros prestados."

        resultado = f"Libros prestados a {self.nombre}:\n"
        for libro in self.libros_prestados:
            resultado += f"- {libro.titulo} (ISBN: {libro.isbn})\n"
        return resultado

    def __str__(self):
        # Representación en string del usuario
        return f"Usuario: {self.nombre} | ID: {self.usuario_id} | Libros prestados: {len(self.libros_prestados)}"


# Definición de la clase Biblioteca
class Biblioteca:
    def __init__(self):
        # Diccionario para almacenar libros con ISBN como clave
        self.libros = {}
        # Diccionario para almacenar usuarios con ID como clave
        self.usuarios = {}
        # Conjunto para mantener los IDs de usuario únicos
        self.ids_usuarios = set()

    def añadir_libro(self, titulo, autor, categoria, isbn):
        # Verifica si el ISBN ya existe en la biblioteca
        if isbn in self.libros:
            return f"Error: Ya existe un libro con el ISBN {isbn}"

        # Crea un nuevo libro y lo añade al diccionario
        nuevo_libro = Libro(titulo, autor, categoria, isbn)
        self.libros[isbn] = nuevo_libro
        return f"Libro '{titulo}' añadido con éxito."

    def quitar_libro(self, isbn):
        # Elimina un libro de la biblioteca por su ISBN
        if isbn not in self.libros:
            return f"Error: No existe un libro con el ISBN {isbn}"

        # Verificamos que el libro no esté prestado
        if not self.libros[isbn].disponible:
            return f"Error: El libro con ISBN {isbn} está prestado actualmente y no puede ser eliminado."

        # Eliminamos el libro del diccionario
        libro_eliminado = self.libros.pop(isbn)
        return f"Libro '{libro_eliminado.titulo}' eliminado con éxito."

    def registrar_usuario(self, nombre, usuario_id):
        # Verifica si el ID de usuario ya existe
        if usuario_id in self.ids_usuarios:
            return f"Error: Ya existe un usuario con el ID {usuario_id}"

        # Crea un nuevo usuario y lo añade a los diccionarios y conjuntos
        nuevo_usuario = Usuario(nombre, usuario_id)
        self.usuarios[usuario_id] = nuevo_usuario
        self.ids_usuarios.add(usuario_id)
        return f"Usuario '{nombre}' registrado con éxito."

    def dar_baja_usuario(self, usuario_id):
        # Elimina un usuario de la biblioteca
        if usuario_id not in self.ids_usuarios:
            return f"Error: No existe un usuario con el ID {usuario_id}"

        # Verificamos que el usuario no tenga libros prestados
        if self.usuarios[usuario_id].libros_prestados:
            return f"Error: El usuario tiene libros prestados y no puede ser dado de baja."

        # Eliminamos el usuario del diccionario y del conjunto
        usuario_eliminado = self.usuarios.pop(usuario_id)
        self.ids_usuarios.remove(usuario_id)
        return f"Usuario '{usuario_eliminado.nombre}' dado de baja con éxito."

    def prestar_libro(self, isbn, usuario_id):
        # Verifica que existan tanto el libro como el usuario
        if isbn not in self.libros:
            return f"Error: No existe un libro con el ISBN {isbn}"

        if usuario_id not in self.ids_usuarios:
            return f"Error: No existe un usuario con el ID {usuario_id}"

        libro = self.libros[isbn]
        usuario = self.usuarios[usuario_id]

        # Verifica que el libro esté disponible
        if not libro.disponible:
            return f"Error: El libro '{libro.titulo}' no está disponible actualmente."

        # Marca el libro como no disponible
        libro.disponible = False
        # Añade el libro a la lista de préstamos del usuario
        usuario.prestar_libro(libro)
        return f"Libro '{libro.titulo}' prestado con éxito a {usuario.nombre}."

    def devolver_libro(self, isbn, usuario_id):
        # Verifica que existan tanto el libro como el usuario
        if isbn not in self.libros:
            return f"Error: No existe un libro con el ISBN {isbn}"

        if usuario_id not in self.ids_usuarios:
            return f"Error: No existe un usuario con el ID {usuario_id}"

        libro = self.libros[isbn]
        usuario = self.usuarios[usuario_id]

        # Intenta devolver el libro
        libro_devuelto = usuario.devolver_libro(isbn)
        if not libro_devuelto:
            return f"Error: El usuario {usuario.nombre} no tiene prestado el libro con ISBN {isbn}"

        # Marca el libro como disponible nuevamente
        libro.disponible = True
        return f"Libro '{libro.titulo}' devuelto con éxito por {usuario.nombre}."

    def buscar_libros_por_titulo(self, titulo):
        # Busca libros que contengan el texto en el título
        resultados = []
        for libro in self.libros.values():
            if titulo.lower() in libro.titulo.lower():
                resultados.append(libro)
        return resultados

    def buscar_libros_por_autor(self, autor):
        # Busca libros que coincidan con el autor
        resultados = []
        for libro in self.libros.values():
            if autor.lower() in libro.autor.lower():
                resultados.append(libro)
        return resultados

    def buscar_libros_por_categoria(self, categoria):
        # Busca libros de una categoría específica
        resultados = []
        for libro in self.libros.values():
            if categoria.lower() in libro.categoria.lower():
                resultados.append(libro)
        return resultados

    def listar_libros_prestados(self, usuario_id=None):
        # Lista los libros prestados, ya sea de un usuario específico o de todos
        if usuario_id:
            if usuario_id not in self.ids_usuarios:
                return f"Error: No existe un usuario con el ID {usuario_id}"
            return self.usuarios[usuario_id].listar_libros_prestados()

        # Si no se especifica un usuario, muestra todos los libros prestados
        libros_prestados = []
        for usuario in self.usuarios.values():
            for libro in usuario.libros_prestados:
                libros_prestados.append((libro, usuario))

        if not libros_prestados:
            return "No hay libros prestados actualmente."

        resultado = "Libros prestados actualmente:\n"
        for libro, usuario in libros_prestados:
            resultado += f"- {libro.titulo} (ISBN: {libro.isbn}) prestado a {usuario.nombre}\n"
        return resultado


# Ejemplo de uso del sistema
if __name__ == "__main__":
    # Creamos una nueva biblioteca
    biblioteca = Biblioteca()

    # Añadimos algunos libros
    biblioteca.añadir_libro("Don Quijote de la Mancha", "Miguel de Cervantes", "Clásico", "9788420412146")
    biblioteca.añadir_libro("Cien años de soledad", "Gabriel García Márquez", "Realismo mágico", "9788437604947")
    biblioteca.añadir_libro("El principito", "Antoine de Saint-Exupéry", "Infantil", "9788478886296")

    # Registramos algunos usuarios
    biblioteca.registrar_usuario("Ana García", "U001")
    biblioteca.registrar_usuario("Carlos López", "U002")

    # Prestamos libros
    print(biblioteca.prestar_libro("9788420412146", "U001"))
    print(biblioteca.prestar_libro("9788437604947", "U002"))

    # Consultamos los libros prestados
    print(biblioteca.listar_libros_prestados())

    # Devolvemos un libro
    print(biblioteca.devolver_libro("9788420412146", "U001"))

    # Búsqueda de libros
    print("Búsqueda por autor 'Cervantes':")
    for libro in biblioteca.buscar_libros_por_autor("Cervantes"):
        print(libro)