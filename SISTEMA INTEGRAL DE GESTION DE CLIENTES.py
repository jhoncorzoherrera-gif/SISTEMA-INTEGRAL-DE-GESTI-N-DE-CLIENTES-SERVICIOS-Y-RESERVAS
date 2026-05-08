"""
=========================================================
SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
Empresa: Software FJ
Curso: Programación
Autor: [Jhon Alexander Corzo Herrera /Grupo:2201]
Descripción:
Proyecto orientado a objetos SIN base de datos, usando listas,
manejo de archivos para logs y manejo avanzado de excepciones.
=========================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re


# =========================================================
# LOGGER
# =========================================================
def registrar_log(mensaje):
    """Registra eventos y errores en archivo de texto."""
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{fecha}] {mensaje}\n")


# =========================================================
# EXCEPCIONES PERSONALIZADAS
# =========================================================
class SistemaError(Exception):
    """Excepción base del sistema."""
    pass


class ValidacionError(SistemaError):
    """Error en validaciones."""
    pass


class ServicioNoDisponibleError(SistemaError):
    """Servicio no disponible."""
    pass


class ReservaError(SistemaError):
    """Problemas al crear/procesar reservas."""
    pass


# =========================================================
# CLASE ABSTRACTA GENERAL
# =========================================================
class Entidad(ABC):
    def __init__(self, codigo):
        self.codigo = codigo

    @abstractmethod
    def mostrar_info(self):
        pass


# =========================================================
# CLIENTE
# =========================================================
class Cliente(Entidad):
    def __init__(self, codigo, nombre, correo, telefono):
        super().__init__(codigo)
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono
        self.validar_datos()

    # Encapsulación (getters)
    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def validar_datos(self):
        if len(self.__nombre.strip()) < 3:
            raise ValidacionError("El nombre debe tener mínimo 3 caracteres.")

        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, self.__correo):
            raise ValidacionError("Correo electrónico inválido.")

        if not self.__telefono.isdigit() or len(self.__telefono) < 7:
            raise ValidacionError("Teléfono inválido.")

    def mostrar_info(self):
        return f"Cliente: {self.nombre} | Correo: {self.correo} | Teléfono: {self.telefono}"


# =========================================================
# CLASE ABSTRACTA SERVICIO
# =========================================================
class Servicio(Entidad, ABC):
    def __init__(self, codigo, nombre, tarifa_base):
        super().__init__(codigo)
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.validar()

    def validar(self):
        if self.tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser mayor a 0.")

    @abstractmethod
    def calcular_costo(self, cantidad, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass


# =========================================================
# SERVICIOS DERIVADOS
# =========================================================
class ReservaSala(Servicio):
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        subtotal = self.tarifa_base * horas
        total = subtotal + (subtotal * impuesto) - descuento
        return total

    def describir_servicio(self):
        return f"Reserva de Sala - Tarifa por hora: ${self.tarifa_base}"

    def mostrar_info(self):
        return self.describir_servicio()


class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias, impuesto=0, descuento=0):
        subtotal = self.tarifa_base * dias
        total = subtotal + (subtotal * impuesto) - descuento
        return total

    def describir_servicio(self):
        return f"Alquiler de Equipo - Tarifa por día: ${self.tarifa_base}"

    def mostrar_info(self):
        return self.describir_servicio()


class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        subtotal = self.tarifa_base * horas
        total = subtotal + (subtotal * impuesto) - descuento
        return total

    def describir_servicio(self):
        return f"Asesoría Especializada - Tarifa por hora: ${self.tarifa_base}"

    def mostrar_info(self):
        return self.describir_servicio()


# =========================================================
# RESERVA
# =========================================================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

        if duracion <= 0:
            raise ReservaError("La duración debe ser mayor que 0.")

    def confirmar(self):
        if self.estado == "Cancelada":
            raise ReservaError("No se puede confirmar una reserva cancelada.")
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def procesar(self):
        """
        try / except / else / finally
        + encadenamiento de excepciones
        """
        try:
            costo = self.servicio.calcular_costo(
                self.duracion,
                impuesto=0.19,
                descuento=10
            )

            if costo <= 0:
                raise ValueError("Costo inconsistente.")

        except ValueError as e:
            raise ReservaError("Error al calcular la reserva.") from e

        except Exception as e:
            registrar_log(f"ERROR inesperado procesando reserva: {e}")
            raise

        else:
            self.confirmar()
            registrar_log(
                f"Reserva confirmada | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Total: ${costo:.2f}"
            )
            return costo

        finally:
            registrar_log("Proceso de reserva finalizado.")


# =========================================================
# SISTEMA PRINCIPAL
# =========================================================
class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)
        registrar_log(f"Cliente agregado: {cliente.nombre}")

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        registrar_log(f"Servicio agregado: {servicio.nombre}")

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)
        registrar_log("Reserva registrada.")


# =========================================================
# SIMULACIÓN (10+ OPERACIONES)
# =========================================================
def simulacion():
    sistema = SistemaGestion()

    print("\n========== INICIANDO SISTEMA SOFTWARE FJ ==========\n")

    operaciones = [
        lambda: sistema.agregar_cliente(Cliente("C1", "Juan Pérez", "juan@gmail.com", "3201234567")),
        lambda: sistema.agregar_cliente(Cliente("C2", "Ana", "ana_correo_mal", "123")),  # error
        lambda: sistema.agregar_cliente(Cliente("C3", "Carlos Ruiz", "carlos@gmail.com", "3157778888")),

        lambda: sistema.agregar_servicio(ReservaSala("S1", "Sala Premium", 100)),
        lambda: sistema.agregar_servicio(AlquilerEquipo("S2", "Portátil Gamer", 150)),
        lambda: sistema.agregar_servicio(AsesoriaEspecializada("S3", "Consultoría TI", 200)),
        lambda: sistema.agregar_servicio(ReservaSala("S4", "Sala Económica", -10)),  # error

        lambda: sistema.agregar_reserva(
            Reserva(sistema.clientes[0], sistema.servicios[0], 3)
        ),

        lambda: sistema.agregar_reserva(
            Reserva(sistema.clientes[1], sistema.servicios[1], 2)
        ),

        lambda: sistema.agregar_reserva(
            Reserva(sistema.clientes[0], sistema.servicios[2], -1)
        ),  # error

        lambda: sistema.agregar_reserva(
            Reserva(sistema.clientes[0], sistema.servicios[1], 5)
        ),
    ]

    # Ejecutar operaciones controlando errores
    for i, operacion in enumerate(operaciones, start=1):
        print(f"Operación #{i}")

        try:
            operacion()

        except SistemaError as e:
            print("Error controlado:", e)
            registrar_log(f"ERROR CONTROLADO: {e}")

        except Exception as e:
            print("Error inesperado:", e)
            registrar_log(f"ERROR INESPERADO: {e}")

        else:
            print("Operación exitosa")

        finally:
            print("-" * 50)

    print("\n========== PROCESANDO RESERVAS ==========\n")

    for reserva in sistema.reservas:
        try:
            total = reserva.procesar()
            print(
                f"Reserva de {reserva.cliente.nombre} "
                f"confirmada. Total = ${total:.2f}"
            )

        except Exception as e:
            print("No se pudo procesar reserva:", e)
            registrar_log(f"FALLO EN RESERVA: {e}")

    print("\n========== RESUMEN ==========")
    print("Clientes registrados:", len(sistema.clientes))
    print("Servicios registrados:", len(sistema.servicios))
    print("Reservas registradas:", len(sistema.reservas))
    print("\nRevise el archivo logs.txt para eventos y errores.")


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    simulacion()
