import sys


def main() -> None:
    # comprueba los argumentos
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
        return

    config: str = sys.argv[1]

    try:
        # Intentamos abrir el archivo
        archivo = open(config, "r")

        # Leemos la primerísima línea
        linea: str = archivo.readline()

        # Mientras no lleguemos al final del archivo (que nos devuelve un texto vacío)
        while linea != "":
            # Quitamos espacios en blanco o saltos de línea a los lados
            linea_limpia: str = linea.strip()

            # Solo hacemos caso si la línea tiene algo y no es un comentario (#)
            if linea_limpia != "" and linea_limpia[0] != "#":
                print("Línea válida encontrada: " + linea_limpia)

            # Avanzamos a la siguiente línea
            linea = archivo.readline()

        archivo.close()
    except FileNotFoundError:
        print("Error: No encuentro el archivo " + config)
    except Exception:
        print("Error: Hubo un problema misterioso al leer el archivo.")


if __name__ == "__main__":
    main()
