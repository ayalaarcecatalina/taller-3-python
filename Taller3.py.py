#--------Subprogramas-------

#def: para subprogramas

def mostrar_menu():
    print("\nBienvenido al Sistema de Gestión de Dispositivos")
    print("\nMenú:")
    print("\nOpción 1: Agregar Dispositivo")
    print("\nOpción 2: Eliminar Dispositivo")
    print("\nOpción 3: Modificar Dispositivo")
    print("\nOpción 4: Listar Todos los Dispositivos")
    print("\nOpción 5: Salir")


def agregar_dispositivo(dispositivos, siguiente_id):
    
    #Solicita datos de un dispositivo; le asigna ID único e incremental; lo guarda en la lista. Retorna el nuevo contador de ID.

    print("\nAgregar Dispositivo")
    nombre = input("\nIngrese el nombre: ")
    tipo = input("\nIngrese el tipo: ")
    fabricante = input("\nIngrese el fabricante: ")

    #Entre llaves: Diccionario
    #Representa un solo dispositivo
    #Es una estructura de datos
    #Guarda la información emparejada en campos (clave:valor)
    nuevo_dispositivo = {
        "id": siguiente_id,
        "nombre": nombre,
        "tipo": tipo,
        "fabricante": fabricante
    }

    #append(): Lista
    #Agrega un nuevo elemento a una lista existente
    dispositivos.append(nuevo_dispositivo)
    print(f"\nDispositivo agregado. ID asignado: {siguiente_id}")
    
    #Retornamos el id incrementado para actualizar la variable externa
    #Contador incremental
    return siguiente_id + 1


def eliminar_dispositivo(dispositivos):
    
    #Busca un dispositivo por su ID y lo elimina de la lista, si existe
    
    #len(): cuenta los elementos de una estructura de datos
    print("\nEliminar Dispositivo")
    if len(dispositivos) == 0:
        print("\nNo hay dispositivos registrados para eliminar")
        return

    id_ingresado = input("Ingrese el ID del dispositivo a eliminar: ")

    #isdigit(): para comprobar si una cadena esta formada solo por dígitos
    #Devuelve V o F
    if not id_ingresado.isdigit():
        print("\nEl ID debe ser un número entero válido.")
        return

    #d: variable de control
    id_buscar = int(id_ingresado)
    for d in dispositivos:
        if d["id"] == id_buscar:
            dispositivos.remove(d)
            print(f"\nDispositivo con ID {id_buscar} eliminado correctamente")
            return

    print(f"\nNo se encontró ningún dispositivo con ID {id_buscar}")


def modificar_dispositivo(dispositivos):

    #Permite editar los campos de un dispositivo existente identificado por su ID
    
    print("\nModificar Dispositivo")
    if len(dispositivos) == 0:
        print("[INFO] No hay dispositivos registrados para modificar.")
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

            #strip(): elimina espacios en blanco, caracteres invisibles y tabulaciones
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
    
    #Muestra en formato de tabla todos los dispositivos almacenados

    print("\nLista de Dispositivos")
    if len(dispositivos) == 0:
        print("\nNo hay dispositivos almacenados")
        return

    print("-" * 60)
    print(f"{'ID':<5} | {'NOMBRE':<20} | {'TIPO':<15} | {'FABRICANTE':<15}")
    print("-" * 60)

    for d in dispositivos:
        print(f"{d['id']:<5} | {d['nombre']:<20} | {d['tipo']:<15} | {d['fabricante']:<15}")

    print("-" * 60)

#-------Cuerpo Principal-------

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


# Punto de entrada al programa
#Ésto permite reutilización de código (Módulos / Importaciones)
if __name__ == "__main__":
    main()