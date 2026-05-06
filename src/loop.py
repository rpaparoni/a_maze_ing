# src/graphics.py
from mlx import Mlx
from typing import Dict # Importamos Dict para las pistas de tipos

# Le decimos: "Vas a recibir un parámetro llamado 'config' que es un diccionario"
def init_graphics(config: Dict[str, str]) -> None:
    print("Starting mlx...")
    connection = mlx_init()
    
    if not connection:
        print("Error: Could not connect to the graphical system.")
        return

    # IMPORTANTE: Los datos del config son texto (str). 
    # Para el tamaño de la ventana necesitamos números enteros (int).
    # Además, WIDTH es el número de celdas, ¡no de píxeles! 
    # Si cada celda mide 30 píxeles, multiplicamos:
    
    celdas_ancho: int = int(config["WIDTH"])
    celdas_alto: int = int(config["HEIGHT"])
    tamano_celda: int = 30
    
    ancho_ventana: int = celdas_ancho * tamano_celda
    alto_ventana: int = celdas_alto * tamano_celda

    print("Opening window...")
    # Usamos nuestras nuevas variables numéricas para el tamaño
    window = mlx_new_window(connection, ancho_ventana, alto_ventana, "A-Maze-ing")
    
    if not window:
        print("Error: Could not create the window.")
        return

    print("Window ready!")
    mlx_loop(connection)
