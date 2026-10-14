#taller 8
from abc import ABC, abstractmethod


class CuentaBancaria(ABC):
    def __init__(self, titular: str, numero_cuenta: str, saldo: float = 0):
        self.titular = titular
        self.numero_cuenta = numero_cuenta
        self.__saldo = saldo

    @property
    def saldo(self) -> float:
        return self.__saldo

    def depositar(self, monto: float) -> bool:
        if monto <= 0:
            return False
        self.__saldo += monto
        return True

    def _descontar_saldo(self, monto: float) -> bool:
        if monto <= 0:
            return False
        self.__saldo -= monto
        return True

    @abstractmethod
    def extraer(self, monto: float) -> bool:
        pass


class CajaAhorro(CuentaBancaria):
    def extraer(self, monto: float) -> bool:
        if monto <= 0 or self.saldo < monto:
            return False
        return self._descontar_saldo(monto)


class CuentaCorriente(CuentaBancaria):
    def __init__(
        self,
        titular: str,
        numero_cuenta: str,
        limite_descubierto: float,
        saldo: float = 0,
    ):
        super().__init__(titular, numero_cuenta, saldo)
        self.limite_descubierto = limite_descubierto

    def extraer(self, monto: float) -> bool:
        if monto <= 0 or monto > self.saldo + self.limite_descubierto:
            return False
        return self._descontar_saldo(monto)


def procesar_extracciones(cuentas: list, monto: float) -> list:
    return [cuenta.extraer(monto) for cuenta in cuentas]


def main():
    cantidad = int(input("¿Cuántas cuentas desea ingresar? "))
    cuentas = []

    for indice in range(cantidad):
        print(f"\nCuenta {indice + 1}")
        tipo = input("Tipo (1: Caja de ahorro, 2: Cuenta corriente): ").strip()
        titular = input("Titular: ").strip()
        numero_cuenta = input("Número de cuenta: ").strip()
        saldo = float(input("Saldo inicial: "))

        if tipo == "1":
            cuenta = CajaAhorro(titular, numero_cuenta, saldo)
        elif tipo == "2":
            limite = float(input("Límite de descubierto: "))
            cuenta = CuentaCorriente(titular, numero_cuenta, limite, saldo)
        else:
            print("Tipo de cuenta inválido; se omitirá esta cuenta.")
            continue

        cuentas.append(cuenta)

    if not cuentas:
        print("No hay cuentas para procesar.")
        return

    monto = float(input("\nMonto a extraer de cada cuenta: "))
    resultados = procesar_extracciones(cuentas, monto)

    print("\nResultado de las extracciones:")
    for cuenta, extraida in zip(cuentas, resultados):
        estado = "realizada" if extraida else "rechazada"
        print(
            f"{cuenta.titular} (cuenta {cuenta.numero_cuenta}): "
            f"extracción {estado}; saldo actual: {cuenta.saldo:.2f}"
        )


if __name__ == "__main__":
    main()
