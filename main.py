import json
import os
import sys
from pathlib import Path

clear = lambda: os.system('cls')
ruta = Path(__file__).parent / "inventario.json"

# Funcion que espera a interaccion del usuario
def continuar():
    input('Pulsa "Enter" para continuar.')

# Comprobacion de si el articulo existe
def comprobarArticulo(item):
    return item in inventario

# Funcion para controlar los movimientos que introduce el usuario
def inputMovimiento():
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
#Funcion para controlar las opciones del menu
def inputMenu():
    try:
        return int(input("Selecciona una opcion: "))
    except ValueError:
        print("Caracter no valido, introduzca solo numeros")
        continuar()
        return None
#Funcion para controlar los articulos
def inputArticulo():
    articulo = input("Introduce el articulo: ")
    articulo = articulo.upper().strip()
    if articulo:
        return articulo
    else:
        print("Articulo no válido")
        continuar()
        return None
#Actualizar fichero
def guardar():
    json_data = json.dumps(inventario,indent=4)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(json_data)

#Primero revisamos si el fichero existe. Si no existe lo creamos.
if not ruta.exists():
    ruta.write_text("{}", encoding="utf-8")

#Luego revisamos si tiene contenido. Si no, generamos un dict vacio.
fichero = ruta.read_text(encoding="utf-8").strip()
try:
    inventario = json.loads(fichero) if fichero else {}
except json.JSONDecodeError as e:
    print(f"Error al cargar el fichero {ruta}. Error: {e}")
    continuar()
    sys.exit(1)

def main():
    #Menu principal
    while True:
        clear()
        print("StockFlow")
        print("1. Mostrar inventario.")
        print("2. Añadir articulo")
        print("3. Eliminar articulo")
        print("4. Operaciones")
        print("0. Salir")

        menu = inputMenu()
        if menu is None:
            continue

        if menu == 0:
            print("Saliendo...")
            break
        elif menu == 1:
            clear()
            if len(inventario) == 0:
                print("El inventario esta vacio")
            else:
                for item, stock in inventario.items():
                    print (f"{item} : {stock}")
            continuar()
        elif menu == 2:
            clear()
            item = inputArticulo()
            if item is not None:
                if comprobarArticulo(item):
                    print("El articulo ya existe. Introduce otro articulo.")
                    continuar()
                else:
                    inventario[item] = 0
                    print(f"Añadido el articulo: {item}")
                    guardar()
                    continuar()
        elif menu == 3:
            clear()
            item = inputArticulo()
            if item is not None:
                if not comprobarArticulo(item):
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
            #Submenu Movimientos
            item = inputArticulo()
            if item is not None:
                if comprobarArticulo(item):
                    while True:
                        clear()
                        print("## OPERACIONES ##")
                        print("1. Entrada")
                        print("2. Salida")
                        print("0. Volver")

                        submenu = inputMenu()
                        if submenu is None:
                            continue

                        if submenu == 0:
                            clear()
                            print("Volviendo...")
                            continuar()
                            break
                        elif submenu == 1:
                            movimiento = inputMovimiento()
                            if movimiento is None:
                                continue
                            else:
                                inventario[item] = inventario[item] + movimiento
                                print(f"Se han añadido {movimiento} unidades de {item}.")
                                guardar()
                                continuar()
                        elif submenu == 2:
                            movimiento = inputMovimiento()
                            if movimiento is None:
                                continue
                            else:
                                stock = inventario[item]
                                if movimiento > stock:
                                    print("No quedan tantas unidades")
                                else:
                                    inventario[item] = inventario[item] - movimiento
                                    print(f"Se han restado {movimiento} unidades de {item}.")
                                    guardar()
                            continuar()
                        else:
                            clear()
                            print("Valor no reconocido. Seleccione una opcion válida")
                            continuar()
                else:
                    print ("El articulo no existe.")
                    continuar()
        else:
            clear()
            print("Valor no reconocido. Seleccione una opcion válida")
            continuar()

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
       print("Saliendo del programa")
