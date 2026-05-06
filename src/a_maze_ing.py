import sys
from typing import Dict, List
from loop import init_graphics


def parsing(file: str) -> Dict[str, str]:
    # Aquí guardaremos nuestras parejas de CLAVE y VALOR
    config: Dict[str, str] = {}

    try:
        archivo = open(file, "r")
        line: str = archivo.readline()

        # Nuestro fiel while para recorrer el archivo
        while line != "":
            line_limpia: str = line.strip()

            # Si no está vacía y no es un comentario (#), la procesamos
            if line_limpia != "" and line_limpia[0] != "#":

                # Partimos la línea usando el signo igual
                partes: List[str] = line_limpia.split("=")

                # Nos aseguramos de que haya exactamente dos partes (Clave y Valor)
                if len(partes) == 2:
                    clave: str = partes[0].strip()
                    valor: str = partes[1].strip()

                    # Guardamos en nuestro diccionario
                    config[clave] = valor
                else:
                    print("Advertencia: Línea con formato raro ignorada -> " + line_limpia)

            # No olvidemos avanzar a la siguiente línea para que el while no sea infinito
            line = archivo.readline()

        archivo.close()

    except FileNotFoundError:
        print("Error: No encuentro el archivo " + file)
    except Exception:
        print("Error: Ocurrió un problema inesperado leyendo el archivo.")

    return config


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: Uso correcto -> python3 a_maze_ing.py config.txt")
        return

    config_txt: str = sys.argv[1]

    # Llamamos a nuestro parseador y guardamos el resultado
    config_data: Dict[str, str] = parsing(config_txt)
    init_graphics(config_data)


if __name__ == "__main__":
    main()
