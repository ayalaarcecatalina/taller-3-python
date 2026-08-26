def Abm():
    print("")
    print("============================================================================================")
    print("Bienvenidos al menu de ABM (Alta, Baja, Modificación) de Dispositivos de Telecomunicaciones")
    print("Elija una de las opciones")
    print("")
    print("1. Agregar Dispositivo")
    print("2. Eliminar Dispositivo")
    print("3. Modificar Dispositivo")
    print("4. Listar todos los Dispositivos")
    print("5. Salir")
    print("Elija una de las opciones")
    print("============================================================================================")
    print("")

def agregar():
    print("Elegiste la opcion: 1.AGREGAR DISPOSITIVO")

def eliminar():
    print("Elegiste la opcion: 2.ELIMINAR DISPOSITIVO")

def modificar():
    print("Elegiste la opcion: 3.MODIFICAR DISPOSITIVO")

def listar():
    print("Elegiste la opcion: 4.LISTAR DISPOSITIVOS")

def salir():
    print("Elegiste la opcion: 5. SALIR")
    print("Hasta luego!")

def error():
    print("Elija una opcion valida")

Abm()

opcion = int(input())


if opcion==1:
    agregar()
elif opcion==2:
    eliminar()
elif opcion==3:
    modificar()
elif opcion==4:
    listar()
elif opcion==5:
    salir()
else:
    error()
