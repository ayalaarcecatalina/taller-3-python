# Taller 4 - Sistema de Gestión de Dispositivos


class Dispositivo:
    def __init__(self, id_dispositivo, nombre, tipo, fabricante):
        self.id = id_dispositivo
        self.nombre = nombre
        self.tipo = tipo
        self.fabricante = fabricante


def mostrar_menu():
    print("Menu:")
    print("1. Agregar Dispositivo")
    print("2. Eliminar Dispositivo")
    print("3. Modificar Dispositivo")
    print("4. Listar Dispositivos")
    print("5. Listar Dispositivos Eliminados")
    print("6. Recuperar Dispositivo Eliminado")
    print("7. Salir")


def agregar_dispositivo(dispositivos, idsiguiente):
    nombre = input("Ingrese el nombre del dispositivo: ")
    tipo = input("Ingrese el tipo de dispositivo: ")
    fabricante = input("Ingrese el fabricante del dispositivo: ")

    dispositivo = Dispositivo(idsiguiente, nombre, tipo, fabricante)
    dispositivos.append(dispositivo)
    print("Dispositivo agregado exitosamente.")
    return idsiguiente + 1


def guardar_id_eliminado(eliminados, dispositivo):
    eliminado = {
        "id": dispositivo.id,
        "nombre": dispositivo.nombre,
        "tipo": dispositivo.tipo,
        "fabricante": dispositivo.fabricante
    }
    eliminados.append(eliminado)


def eliminar_dispositivo(dispositivos, eliminados):
    if not dispositivos:
        print("No hay dispositivos para eliminar.")
        return

    id_buscar = int(input("Ingrese el ID del dispositivo a eliminar: "))

    for dispositivo in dispositivos:
        if dispositivo.id == id_buscar:
            dispositivos.remove(dispositivo)
            guardar_id_eliminado(eliminados, dispositivo)
            print("Dispositivo eliminado exitosamente.")
            return

    print("Dispositivo no encontrado.")


def modificar_dispositivo(dispositivos):
    if not dispositivos:
        print("No hay dispositivos para modificar.")
        return

    id_buscar = int(input("Ingrese el ID del dispositivo a modificar: "))

    for dispositivo in dispositivos:
        if dispositivo.id == id_buscar:
            print("Actualizando datos del dispositivo con ID", dispositivo.id)
            dispositivo.nombre = input("Nuevo nombre: ")
            dispositivo.tipo = input("Nuevo tipo: ")
            dispositivo.fabricante = input("Nuevo fabricante: ")
            print("Dispositivo modificado exitosamente.")
            return

    print("Dispositivo no encontrado.")


def listar_dispositivos(dispositivos):
    if not dispositivos:
        print("No hay dispositivos registrados.")
        return

    print("\nLista de dispositivos:")
    for dispositivo in dispositivos:
        print(f"ID: {dispositivo.id} | Nombre: {dispositivo.nombre} | Tipo: {dispositivo.tipo} | Fabricante: {dispositivo.fabricante}")


def listar_dispositivos_eliminados(eliminados):
    if not eliminados:
        print("No hay dispositivos eliminados.")
        return

    print("\nLista de dispositivos eliminados:")
    for dispositivo in eliminados:
        print(f"ID: {dispositivo['id']} | Nombre: {dispositivo['nombre']} | Tipo: {dispositivo['tipo']} | Fabricante: {dispositivo['fabricante']}")


def recuperar_dispositivo(dispositivos, eliminados):
    if not eliminados:
        print("No hay dispositivos eliminados para recuperar.")
        return

    id_buscar = int(input("Ingrese el ID del dispositivo a recuperar: "))

    for dispositivo in eliminados:
        if dispositivo["id"] == id_buscar:
            dispositivo_recuperado = Dispositivo(
                dispositivo["id"],
                dispositivo["nombre"],
                dispositivo["tipo"],
                dispositivo["fabricante"]
            )
            dispositivos.append(dispositivo_recuperado)
            eliminados.remove(dispositivo)
            print("Dispositivo recuperado exitosamente.")
            return

    print("Dispositivo eliminado no encontrado.")


# Cuerpo principal del programa
def main():
    dispositivos = []
    eliminados = []
    idsiguiente = 1
    print("Bienvenido al Sistema de Gestión de Dispositivos")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            idsiguiente = agregar_dispositivo(dispositivos, idsiguiente)
        elif opcion == "2":
            eliminar_dispositivo(dispositivos, eliminados)
        elif opcion == "3":
            modificar_dispositivo(dispositivos)
        elif opcion == "4":
            listar_dispositivos(dispositivos)
        elif opcion == "5":
            listar_dispositivos_eliminados(eliminados)
        elif opcion == "6":
            recuperar_dispositivo(dispositivos, eliminados)
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()