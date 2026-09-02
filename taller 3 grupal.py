#federico_blanc_catalina_ayala_miriam_grecco_uriel_braslavsky

def mostrar_menu():
    print("\nBienvenido al Sistema de Gestión de Dispositivos")
    print("\nMenú:")
    print("\nOpción 1: Agregar Dispositivo")
    print("\nOpción 2: Eliminar Dispositivo")
    print("\nOpción 3: Modificar Dispositivo")
    print("\nOpción 4: Listar Todos los Dispositivos")
    print("\nOpción 5: Salir")


def agregar_dispositivo(dispositivos, siguiente_id):
    
    print("\nAgregar Dispositivo")
    nombre = input("\nIngrese el nombre: ")
    tipo = input("\nIngrese el tipo: ")
    fabricante = input("\nIngrese el fabricante: ")

    nuevo_dispositivo = {
        "id": siguiente_id,
        "nombre": nombre,
        "tipo": tipo,
        "fabricante": fabricante
    }

    dispositivos.append(nuevo_dispositivo)
    print(f"\nDispositivo agregado. ID asignado: {siguiente_id}")
    
    return siguiente_id + 1

def eliminar_dispositivo(dispositivos):
  
    print("\nEliminar Dispositivo")
    if len(dispositivos) == 0:
        print("\nNo hay dispositivos registrados para eliminar")
        return

    id_ingresado = input("Ingrese el ID del dispositivo a eliminar: ")

  
    if not id_ingresado.isdigit():
        print("\nEl ID debe ser un número entero válido.")
        return

    id_buscar = int(id_ingresado)
    for d in dispositivos:
        if d["id"] == id_buscar:
            dispositivos.remove(d)
            print(f"\nDispositivo con ID {id_buscar} eliminado correctamente")
            return

    print(f"\nNo se encontró ningún dispositivo con ID {id_buscar}")


def modificar_dispositivo(dispositivos):

    print("\nModificar Dispositivo")
    if len(dispositivos) == 0:
        print("No hay dispositivos registrados para modificar.")
        return

    id_ingresado = input("Ingrese el ID del dispositivo a modificar: ")

    if not id_ingresado.isdigit():
        print("\nEl ID debe ser un número entero válido")
        return

    id_buscar = int(id_ingresado)
    for d in dispositivos:
        if d["id"] == id_buscar:
            print(f"\nDispositivo encontrado: {d['nombre']}")
            print("\nPresione ENTER sin escribir nada si no desea modificar un campo")

            nuevo_nombre = input(f"Nuevo nombre (actual: {d['nombre']}): ")
            nuevo_tipo = input(f"Nuevo tipo (actual: {d['tipo']}): ")
            nuevo_fabricante = input(f"Nuevo fabricante (actual: {d['fabricante']}): ")

          
            if nuevo_nombre.strip() != "":
                d["nombre"] = nuevo_nombre
            if nuevo_tipo.strip() != "":
                d["tipo"] = nuevo_tipo
            if nuevo_fabricante.strip() != "":
                d["fabricante"] = nuevo_fabricante

            print(f"\nDispositivo con ID {id_buscar} modificado con éxito.")
            return

    print(f"\nNo se encontró ningún dispositivo con ID {id_buscar}.")


def listar_dispositivos(dispositivos):

    print("\nLista de Dispositivos")
    if len(dispositivos) == 0:
        print("\nNo hay dispositivos almacenados")
        return

    print("-" * 18)
    print(f"{'ID'} | {'NOMBRE'} | {'TIPO':} | {'FABRICANTE'}")
    print("-" * 18)

    for d in dispositivos:
        print(f"{d['id']} | {d['nombre']} | {d['tipo']:} | {d['fabricante']}")

    print("-" * 18)
#cuerpo principall
def main():
    dispositivos = []
    siguiente_id = 1
    opcion = ""

    while opcion != "5":
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-5): ")

        if opcion == "1":
            siguiente_id = agregar_dispositivo(dispositivos, siguiente_id)
        elif opcion == "2":
            eliminar_dispositivo(dispositivos)
        elif opcion == "3":
            modificar_dispositivo(dispositivos)
        elif opcion == "4":
            listar_dispositivos(dispositivos)
        elif opcion == "5":
            print("\nSaliendo del sistema")
        else:
            print("\nOpción no válida. Por favor, ingrese una opción válida")

main()
