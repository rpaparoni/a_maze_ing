import sys
from typing import Dict, List

def parsear_configuracion(nombre_archivo: str) -> Dict[str, str]:
    # Aquí guardaremos nuestras parejas de CLAVE y VALOR
    config: Dict[str, str] = {}
    
    try:
        archivo = open(nombre_archivo, "r")
        linea: str = archivo.readline()
        
        # Nuestro fiel while para recorrer el archivo
        while linea != "":
            linea_limpia: str = linea.strip()
            
            # Si no está vacía y no es un comentario (#), la procesamos
            if linea_limpia != "" and linea_limpia[0] != "#":
                
                # Partimos la línea usando el signo igual
                partes: List[str] = linea_limpia.split("=")
                
                # Nos aseguramos de que haya exactamente dos partes (Clave y Valor)
                if len(partes) == 2:
                    clave: str = partes[0].strip()
                    valor: str = partes[1].strip()
                    
                    # Guardamos en nuestro diccionario
                    config[clave] = valor
                else:
                    print("Advertencia: Línea con formato raro ignorada -> " + linea_limpia)
            
            # No olvidemos avanzar a la siguiente línea para que el while no sea infinito
            linea = archivo.readline()
            
        archivo.close()
        
    except FileNotFoundError:
        print("Error: No encuentro el archivo " + nombre_archivo)
    except Exception:
        print("Error: Ocurrió un problema inesperado leyendo el archivo.")
        
    return config


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: Uso correcto -> python3 a_maze_ing.py config.txt")
        return

    archivo_config: str = sys.argv[1]
    
    # Llamamos a nuestro parseador y guardamos el resultado
    mis_datos: Dict[str, str] = parsear_configuracion(archivo_config)
    
    # Imprimimos para comprobar que ha funcionado
    print("¡Parseo exitoso! Estos son los datos puros:")
    print(mis_datos)

if __name__ == "__main__":
    main()
