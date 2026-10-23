#Taller 9

#Los archivos txt, scv y json se crean automáticamente al ejecutar el programa y comenzar a cargar datos
#Se guardan en la carpeta del programa

#Importaciones:

import csv
#Permite leer y escribir en archicos cvs; organiza los datos en filas y columnas tipo excel
#Funciones utilizadas:
#dictwriter(): permite escribir diccionarios como filas
#writeheader(): escribe los nombres de las columnas
#writerow(): agrega una fila con los datos de una jugada
import json
#Importación que permite guardar y recuperar informacion en archivos json
#Funciones utilizadas:
#dump(): guarda los datos en un archivo JSON
#load(): lee los datos de un archivo JSON
#indent=4: organiza el archivo con sangrías para facilitar su lectura
#ensure_ascii=False: permite conservar caracteres como la ñ y las vocales acentuadas
import random
#Permite utilización de aleatoriedad
#Funciones utilizadas:
#random.choice(self.SIMBOLOS): selecciona un símbolo al azar para el tragamonedas
#random.randint(0, 36): genera un número entero aleatorio entre 0 y 36 incluidos para la ruleta
import os
#Permite interactuar con el sistema operativo y consultar información sobre archivos
#Funciones utilizadas:
#os.path.exists("jugadores.json"): comprueba si el archivo existe
#os.path.getsize("historial_apuestas.csv"): devuelve el tamaño del archivo en bytes. Permite comprobar si el CSV está vacío antes de escribir su encabezado
from abc import ABC, abstractmethod
#ABC: permite definir clases base abstractas
#@abstractmethod: permite declarar métodos que deben implementarse en las subclases
from datetime import datetime
#Permite trabajar con fechas y horas
#Funciones utilizadas:
#datetime.now().strftime("%Y-%m-%d %H:%M:%S"): obtiene la fecha y hora actuales en un formato legible (ejemplo: 2026-10-23 18:30:00)
#datetime.now().strftime("%Y%m%d%H%M%S%f"): permite generar un identificador de jugada basado en la fecha, la hora y los microsegundos

#Subprogramas

#Persistencia de datos y auditoría

class Persistencia:
    ARCHIVO_TXT = "auditoria.txt"
    ARCHIVO_CSV = "historial_apuestas.csv"
    ARCHIVO_JSON = "jugadores.json"

    @staticmethod
    def auditar(mensaje):
        #Registra un evento en la bitacora
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(Persistencia.ARCHIVO_TXT, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{fecha}] {mensaje}\n")

    @staticmethod
    def registrar_apuesta(datos):
        #Agrega una jugada al historial csv
        campos = [
            "id_jugada",
            "jugador",
            "juego",
            "monto_apostado",
            "resultado",
            "ganancia",
        ]

        existe = os.path.exists(Persistencia.ARCHIVO_CSV)
        tiene_datos = existe and os.path.getsize(
            Persistencia.ARCHIVO_CSV
        ) > 0

        with open(
            Persistencia.ARCHIVO_CSV,
            "a",
            newline="",
            encoding="utf-8",
        ) as archivo:
            escritor = csv.DictWriter(
                archivo, fieldnames=campos
            )

            if not tiene_datos:
                escritor.writeheader()

            escritor.writerow(datos)

    @staticmethod
    def guardar_jugadores(jugadores):
        #Guarda los perfiles de jugadores en formato json
        datos = [
            {
                "apodo": jugador.apodo,
                "saldo_inicial": jugador.saldo,
                "vip": jugador.vip,
            }
            for jugador in jugadores.values()
        ]

        with open(
            Persistencia.ARCHIVO_JSON,
            "w",
            encoding="utf-8",
        ) as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    @staticmethod
    def cargar_jugadores():
        #Carga los perfiles de jugadores guardados en json
        if not os.path.exists(Persistencia.ARCHIVO_JSON):
            return {}

        try:
            with open(
                Persistencia.ARCHIVO_JSON,
                "r",
                encoding="utf-8",
            ) as archivo:
                datos = json.load(archivo)

            if not isinstance(datos, list):
                raise ValueError("El JSON debe contener una lista.")

            jugadores = {}

            for dato in datos:
                apodo = dato["apodo"]
                saldo = dato["saldo_inicial"]
                vip = dato["vip"]

                if (
                    not isinstance(apodo, str)
                    or not apodo.strip()
                    or type(saldo) not in (int, float)
                    or saldo < 0
                    or not isinstance(vip, bool)
                ):
                    raise ValueError("Perfil de jugador invalido.")

                apodo = apodo.strip()

                if apodo in jugadores:
                    raise ValueError("Hay apodos duplicados.")

                jugadores[apodo] = Jugador(
                    apodo, saldo, vip
                )

            return jugadores

        except (json.JSONDecodeError, KeyError, TypeError,
                ValueError) as error:
            Persistencia.auditar(
                f"Error al cargar jugadores.json: {error}"
            )
            print(f"Error al cargar los perfiles: {error}")
            return {}

#Clase jugador: encapsulamiento

class Jugador:
    def __init__(self, apodo, saldo_inicial=1000, vip=False):
        if not isinstance(apodo, str) or not apodo.strip():
            raise ValueError("El apodo no puede estar vacio.")

        if (
            type(saldo_inicial) not in (int, float)
            or saldo_inicial < 0
        ):
            raise ValueError("El saldo inicial debe ser no negativo.")

        if not isinstance(vip, bool):
            raise ValueError("VIP debe ser True o False.")

        self._apodo = apodo.strip()
        self._saldo = saldo_inicial
        self._vip = vip

    @property
    def apodo(self):
        return self._apodo

    @property
    def saldo(self):
        #Consulta el saldo sin asignarlo directamente
        return self._saldo

    @property
    def vip(self):
        return self._vip

    def depositar(self, cantidad):
        if (
            type(cantidad) not in (int, float)
            or cantidad <= 0
        ):
            raise ValueError("El deposito debe ser positivo.")

        self._saldo += cantidad
        Persistencia.auditar(
            f"{self.apodo} deposito {cantidad} fichas."
        )

    def descontar(self, cantidad):
        if (
            type(cantidad) not in (int, float)
            or cantidad <= 0
        ):
            raise ValueError("La apuesta debe ser positiva.")

        if cantidad > self._saldo:
            raise ValueError("Saldo insuficiente.")

        self._saldo -= cantidad

    def __str__(self):
        categoria = "VIP" if self.vip else "Regular"
        return (
            f"{self.apodo} | Saldo: {self.saldo} fichas "
            f"| Categoria: {categoria}"
        )

#Clase abstracta: juego casino

class JuegoCasino(ABC):
    def __init__(self, nombre, apuesta_minima=10):
        if (
            type(apuesta_minima) not in (int, float)
            or apuesta_minima <= 0
        ):
            raise ValueError("La apuesta minima debe ser positiva.")

        self._nombre = nombre
        self._apuesta_minima = apuesta_minima

    @property
    def nombre(self):
        return self._nombre

    @property
    def apuesta_minima(self):
        return self._apuesta_minima

    @abstractmethod
    def jugar(self, jugador, apuesta, seleccion=None):
        #Cada juego implementa su propia mecánica
        pass

    def _validar_apuesta(self, jugador, apuesta):
        if not isinstance(jugador, Jugador):
            raise TypeError("Se requiere un objeto Jugador.")

        if (
            type(apuesta) not in (int, float)
            or apuesta < self._apuesta_minima
        ):
            raise ValueError(
                f"La apuesta minima es {self._apuesta_minima} fichas."
            )

        if apuesta > jugador.saldo:
            raise ValueError("El jugador no tiene fichas suficientes.")

    def _finalizar_jugada(self, jugador, apuesta, resultado, ganancia):
        #Registra el resultado y devuelve un resumen
        datos = {
            "id_jugada": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "jugador": jugador.apodo,
            "juego": self.nombre,
            "monto_apostado": apuesta,
            "resultado": resultado,
            "ganancia": ganancia,
        }

        Persistencia.auditar(
            f"{jugador.apodo} jugo {self.nombre}: "
            f"apuesta={apuesta}, resultado={resultado}, "
            f"ganancia_neta={ganancia}, saldo={jugador.saldo}."
        )

        return {
            **datos,
            "saldo_final": jugador.saldo,
        }

# Juego tragamonedas

class Tragamonedas(JuegoCasino):
    SIMBOLOS = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]

    def __init__(self, apuesta_minima=10):
        super().__init__("Tragamonedas", apuesta_minima)

    def jugar(self, jugador, apuesta, seleccion=None):
        self._validar_apuesta(jugador, apuesta)
        jugador.descontar(apuesta)

        simbolos = [
            random.choice(self.SIMBOLOS)
            for _ in range(3)
        ]

        if simbolos[0] == simbolos[1] == simbolos[2]:
            #El premio total es cinco veces la apuesta
            premio = apuesta * 5
            ganancia = premio - apuesta
            jugador.depositar(premio)
            resultado = f"PREMIO: {' '.join(simbolos)}"

        elif (
            simbolos[0] == simbolos[1]
            or simbolos[0] == simbolos[2]
            or simbolos[1] == simbolos[2]
        ):
            #Dos símbolos iguales devuelven la apuesta
            premio = apuesta
            ganancia = 0
            jugador.depositar(premio)
            resultado = f"EMPATE: {' '.join(simbolos)}"

        else:
            ganancia = -apuesta
            resultado = f"PERDIDA: {' '.join(simbolos)}"

        return self._finalizar_jugada(
            jugador, apuesta, resultado, ganancia
        )

#Juego ruleta

class Ruleta(JuegoCasino):
    ROJOS = {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36,
    }

    def __init__(self, apuesta_minima=10):
        super().__init__("Ruleta", apuesta_minima)

    def jugar(self, jugador, apuesta, seleccion=None):
        self._validar_apuesta(jugador, apuesta)

        if isinstance(seleccion, bool):
            raise ValueError("Seleccion invalida.")

        if isinstance(seleccion, int):
            if not 0 <= seleccion <= 36:
                raise ValueError("El numero debe estar entre 0 y 36.")
            tipo_apuesta = "numero"

        elif isinstance(seleccion, str):
            seleccion = seleccion.strip().lower()

            if seleccion not in ("rojo", "negro"):
                raise ValueError(
                    "Selecciona un numero (0-36), rojo o negro."
                )
            tipo_apuesta = "color"

        else:
            raise ValueError(
                "Debes indicar un numero entre 0 y 36 o un color."
            )

        jugador.descontar(apuesta)

        numero = random.randint(0, 36)

        if numero == 0:
            color = "verde"
        elif numero in self.ROJOS:
            color = "rojo"
        else:
            color = "negro"

        if tipo_apuesta == "numero" and seleccion == numero:
            #Premio total: 36 veces la apuesta
            premio = apuesta * 36
            ganancia = premio - apuesta
            jugador.depositar(premio)
            estado = "GANADA"

        elif tipo_apuesta == "color" and seleccion == color:
            #Premio total: 2 veces la apuesta
            premio = apuesta * 2
            ganancia = premio - apuesta
            jugador.depositar(premio)
            estado = "GANADA"

        else:
            ganancia = -apuesta
            estado = "PERDIDA"

        resultado = (
            f"{estado}: salio {numero} ({color}); "
            f"seleccion apostada: {seleccion}"
        )

        return self._finalizar_jugada(
            jugador, apuesta, resultado, ganancia
        )

#Cuerpo principal

def solicitar_apuesta(jugador, juego):
    while True:
        try:
            apuesta = float(
                input(
                    f"Apuesta (minimo {juego.apuesta_minima}, "
                    f"saldo {jugador.saldo}): "
                )
            )

            if not apuesta.is_integer():
                print("Utiliza una cantidad entera de fichas.")
                continue

            apuesta = int(apuesta)
            juego._validar_apuesta(jugador, apuesta)
            return apuesta

        except ValueError as error:
            print(f"Error: {error}")


def mostrar_resultado(datos):
    print("\n--- Resultado de la jugada ---")
    print(f"Juego: {datos['juego']}")
    print(f"Resultado: {datos['resultado']}")
    print(f"Ganancia neta: {datos['ganancia']} fichas")
    print(f"Saldo final: {datos['saldo_final']} fichas")
    print("-------------------------------\n")


def main():
    jugadores = Persistencia.cargar_jugadores()

    juegos = {
        "1": Tragamonedas(),
        "2": Ruleta(),
    }

    Persistencia.auditar("Inicio del programa de casino.")

    print("CASINO")

    while True:
        print("\n1. Registrar jugador")
        print("2. Seleccionar jugador")
        print("3. Mostrar jugadores")
        print("4. Guardar y salir")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            apodo = input("Apodo del jugador: ").strip()

            if not apodo:
                print("El apodo no puede estar vacio.")
                continue

            if apodo in jugadores:
                print("Ese apodo ya esta registrado.")
                continue

            try:
                saldo = int(
                    input("Saldo inicial en fichas (0 o mas): ")
                )
                vip_texto = input("Es VIP? (s/n): ").strip().lower()

                if saldo < 0 or vip_texto not in ("s", "n"):
                    raise ValueError("Datos invalidos.")

                jugador = Jugador(
                    apodo,
                    saldo,
                    vip=(vip_texto == "s"),
                )

                jugadores[jugador.apodo] = jugador
                Persistencia.guardar_jugadores(jugadores)
                Persistencia.auditar(
                    f"El jugador {jugador.apodo} se registra."
                )
                print("Jugador registrado correctamente.")

            except ValueError as error:
                print(f"Error: {error}")

        elif opcion == "2":
            apodo = input("Apodo del jugador: ").strip()
            jugador = jugadores.get(apodo)

            if jugador is None:
                print("Jugador no encontrado.")
                continue

            Persistencia.auditar(
                f"El jugador {jugador.apodo} inicia sesion."
            )

            while True:
                print(f"\nJugador: {jugador}")
                print("1. Tragamonedas")
                print("2. Ruleta")
                print("3. Depositar fichas")
                print("4. Volver al menu principal")

                accion = input("Selecciona una opcion: ").strip()

                if accion in juegos:
                    juego = juegos[accion]

                    try:
                        apuesta = solicitar_apuesta(jugador, juego)

                        if isinstance(juego, Ruleta):
                            seleccion_texto = input(
                                "Apuesta a un numero (0-36) "
                                "o color (rojo/negro): "
                            ).strip().lower()

                            if seleccion_texto in ("rojo", "negro"):
                                seleccion = seleccion_texto
                            else:
                                seleccion = int(seleccion_texto)

                            datos = juego.jugar(
                                jugador, apuesta, seleccion
                            )
                        else:
                            datos = juego.jugar(jugador, apuesta)

                        Persistencia.guardar_jugadores(jugadores)
                        mostrar_resultado(datos)

                    except ValueError as error:
                        print(f"No se pudo realizar la jugada: {error}")

                elif accion == "3":
                    try:
                        cantidad = int(
                            input("Cantidad de fichas a depositar: ")
                        )
                        jugador.depositar(cantidad)
                        Persistencia.guardar_jugadores(jugadores)
                        print(f"Nuevo saldo: {jugador.saldo}")
                    except ValueError as error:
                        print(f"Error: {error}")

                elif accion == "4":
                    Persistencia.guardar_jugadores(jugadores)
                    break

                else:
                    print("Opcion no valida.")

        elif opcion == "3":
            if not jugadores:
                print("No hay jugadores registrados.")
            else:
                for jugador in jugadores.values():
                    print(jugador)

        elif opcion == "4":
            Persistencia.guardar_jugadores(jugadores)
            Persistencia.auditar("Cierre del programa de casino.")
            print("Datos guardados. Hasta luego.")
            break

        else:
            print("Opcion no valida.")

if __name__ == "__main__":
    main()