import json
import os
from pathlib import Path

clear = lambda: os.system('cls')
ruta = Path(__file__).parent / "inventario.json"

#Primero revisamos si el fichero existe. Si no existe lo creamos.
if not ruta.exists():
	ruta.write_text("{}", encoding="utf-8")

#Luego revisamos si tiene contenido. Si no, generamos un dict vacio.
fichero = ruta.read_text(encoding="utf-8").strip()
inventario = json.loads(fichero) if fichero else {}

# Funcion que espera a interaccion del usuario
def continuar():
	input('Pulsa "Enter" para continuar.')

# Comprobacion de si el articulo existe
def comprobarArticulo(item):
	return item.upper() in inventario

#Menu principal
while True:
	clear()
	print("StockFlow")
	print("1. Mostrar inventario.")
	print("2. Añadir articulo")
	print("3. Eliminar articulo")
	print("4. Operaciones")
	print("0. Salir")

	try:
		menu = int(input("Selecciona una opcion: "))
	except ValueError:
		print("Caracter no valido, introduzca solo numeros")
		continuar()
		continue

	if menu == 0:
		json_data = json.dumps(inventario,indent=4)
		with open(ruta, "w", encoding="utf-8") as f:
			f.write(json_data)
		clear()
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
		item = input("Introduce el articulo a guardar: ")
		if comprobarArticulo(item):
			print("El articulo ya existe. Introduce otro articulo.")
			continuar()
		else:
			inventario[item.upper()] = 0
			print(f"Añadido el articulo:{item.upper()}")
			continuar()
	elif menu == 3:
		clear()
		item = input("Introduce el articulo a eliminar: ")
		if not comprobarArticulo(item):
			print("El articulo no existe. Introduce otro articulo.")
		else:
			if inventario[item.upper()] > 0:
				print("No se puede eliminar el articulo. Aun le queda stock.")
			else:
				inventario.pop(item.upper())
				print("Articulo eliminado")
		continuar()
	elif menu == 4:
		#Submenu Movimientos
		item = input("Introduce el articulo a Operar: ")
		if comprobarArticulo(item):
			while True:
				clear()
				print("## OPERACIONES ##")
				print("1. Entrada")
				print("2. Salida")
				print("0. Volver")
				try:
					submenu = int(input("Selecciona una opcion: "))
				except ValueError:
					print("Caracter no valido, introduzca solo numeros")
					continuar()
					continue
				if submenu == 0:
					clear()
					print("Volviendo...")
					continuar()
							break
						elif submenu == 1:
							item = input("Introduce el articulo: ")
							if comprobarArticulo(item):
								movimiento = int(input("Introduce la cantidad: "))
								inventario[item.upper()] = inventario[item.upper()] + movimiento
								print(f"Se han añadido {movimiento} unidades de {item.upper()}.")
							else:
								print ("El articulo no existe.")
							continuar()
						elif submenu == 2:
							item = input("Introduce el articulo: ")
							if comprobarArticulo(item):
								movimiento = int(input("Introduce la cantidad: "))
								stock = inventario[item.upper()]
								if movimiento > stock:
									print("No quedan tantas unidades")
								else:
									inventario[item.upper()] = inventario[item.upper()] - movimiento
									print(f"Se han restado {movimiento} unidades.")
							else:
								print ("El articulo no existe.")
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