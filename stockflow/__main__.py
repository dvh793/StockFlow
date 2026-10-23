import json
import os
import sys
from pathlib import Path

ruta = Path(__file__).parent.parent / "datos" / "inventario.json"
inventario = {}


def clear():
    """Limpia la consola."""
    os.system("cls")


def continuar():
    """Espera a que el usuario pulse Enter."""
    input('Pulsa "Enter" para continuar.')


def comprobar_articulo(item):
    """Devuelve True si el articulo existe en el inventario."""
    return item in inventario


def input_movimiento():
    """Pide una cantidad al usuario.

    Devuelve la cantidad si es un entero mayor que 0, o None si no es valida.
    """
    try:
        movimiento = int(input("Introduce la cantidad: "))
    except ValueError:
        print("Caracter no valido, introduzca solo numeros")
        continuar()
        return None
    if movimiento > 0:
        return movimiento
    else:
        print("Valor no valido, debe ser mayor que 0")
        continuar()
        return None


def input_menu():
    """Pide una opcion de menu.

    Devuelve la opcion como entero, o None si no es un numero.
    """
    try:
        return int(input("Selecciona una opcion: "))
    except ValueError:
        print("Caracter no valido, introduzca solo numeros")
        continuar()
        return None


def input_articulo():
    """Pide el nombre de un articulo.

    Devuelve el nombre en mayusculas y sin espacios en los extremos,
    o None si queda vacio.
    """
    articulo = input("Introduce el articulo: ")
    articulo = articulo.upper().strip()
    if articulo:
        return articulo
    else:
        print("Articulo no válido")
        continuar()
        return None


def cargar():
    """Carga el inventario desde el fichero JSON y lo devuelve.

    Si el fichero no existe lo crea vacio. Si esta dañado, avisa y
    cierra el programa sin modificarlo.
    """
    # Primero revisamos si el fichero existe. Si no existe lo creamos.
    if not ruta.exists():
        ruta.write_text("{}", encoding="utf-8")
    # Luego revisamos si tiene contenido. Si no, generamos un dict vacio.
    fichero = ruta.read_text(encoding="utf-8").strip()
    try:
        datos = json.loads(fichero) if fichero else {}
    except json.JSONDecodeError as e:
        print(f"Error al cargar el fichero {ruta}. Error: {e}")
        continuar()
        sys.exit(1)
    return datos


def guardar():
    """Guarda el inventario en el fichero JSON."""
    ruta.write_text(json.dumps(inventario, indent=4), encoding="utf-8")


def main():
    """Muestra el menu principal y gestiona las opciones del usuario."""
    while True:
        clear()
        print("StockFlow")
        print("1. Mostrar inventario.")
        print("2. Añadir articulo")
        print("3. Eliminar articulo")
        print("4. Operaciones")
        print("0. Salir")

        menu = input_menu()
        if menu is None:
            continue

        if menu == 0:
            print("Saliendo...")
            break
        elif menu == 1:
            clear()
            if not inventario:
                print("El inventario esta vacio")
            else:
                for item, stock in inventario.items():
                    print(f"{item} : {stock}")
            continuar()
        elif menu == 2:
            clear()
            item = input_articulo()
            if item is not None:
                if comprobar_articulo(item):
                    print("El articulo ya existe. Introduce otro articulo.")
                    continuar()
                else:
                    inventario[item] = 0
                    print(f"Añadido el articulo: {item}")
                    guardar()
                    continuar()
        elif menu == 3:
            clear()
            item = input_articulo()
            if item is not None:
                if not comprobar_articulo(item):
                    print("El articulo no existe. Introduce otro articulo.")
                else:
                    if inventario[item] > 0:
                        print("No se puede eliminar el articulo. Aun le queda stock.")
                    else:
                        inventario.pop(item)
                        print("Articulo eliminado")
                        guardar()
                continuar()
        elif menu == 4:
            clear()
            # Submenu Movimientos
            item = input_articulo()
            if item is not None:
                if comprobar_articulo(item):
                    while True:
                        clear()
                        print("## OPERACIONES ##")
                        print("1. Entrada")
                        print("2. Salida")
                        print("0. Volver")

                        submenu = input_menu()
                        if submenu is None:
                            continue

                        if submenu == 0:
                            clear()
                            print("Volviendo...")
                            continuar()
                            break
                        elif submenu == 1:
                            movimiento = input_movimiento()
                            if movimiento is None:
                                continue
                            inventario[item] += movimiento
                            print(f"Se han añadido {movimiento} unidades de {item}.")
                            guardar()
                            continuar()
                        elif submenu == 2:
                            movimiento = input_movimiento()
                            if movimiento is None:
                                continue
                            stock = inventario[item]
                            if movimiento > stock:
                                print("No quedan tantas unidades")
                            else:
                                inventario[item] -= movimiento
                                print(
                                    f"Se han restado {movimiento} unidades de {item}."
                                )
                                guardar()
                            continuar()
                        else:
                            clear()
                            print("Valor no reconocido. Seleccione una opcion válida")
                            continuar()
                else:
                    print("El articulo no existe.")
                    continuar()
        else:
            clear()
            print("Valor no reconocido. Seleccione una opcion válida")
            continuar()


if __name__ == "__main__":
    try:
        inventario = cargar()
        main()
    except KeyboardInterrupt:
        """ Si el usuario hace Ctrl + C , mostramos un mensaje de salida."""
        print("Saliendo del programa")
