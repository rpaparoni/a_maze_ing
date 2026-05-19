import sys
from config_parser import parse_config
from graphics_engine import MazeWindow
# Importamos tu nueva clase del archivo mazegen.py
from mazegen import MazeGenerator 

def main() -> None:
    # Verificamos que el usuario nos pase el config.txt
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    # 1. Leemos los datos del archivo de configuración
    config_data = parse_config(sys.argv[1])
    if not config_data:
        return

    # 2. Ponemos a trabajar al Generador (Mordisco 1)
    # Extraemos el tamaño y lo convertimos a entero
    width = int(config_data["WIDTH"])
    height = int(config_data["HEIGHT"])
    
    # Creamos la instancia del generador
    maze = MazeGenerator(height, width)
    
    # Le pedimos que fabrique la cuadrícula llena de paredes
    maze.create_empty_grid()
    
    # Un pequeño mensaje para confirmar que todo va bien
    print(f"Grid initialized with {len(maze.cells)} cells.")
    if width > 10 and height > 10:
        maze.draw_fortytwo()
    maze.carve_passages(0, 0)
    maze.calculate_hex_for_all()
    # 3. Iniciamos la parte gráfica
    # Más adelante le pasaremos el objeto 'maze' a la ventana para que sepa qué pintar
    game = MazeWindow(config_data, maze)
    game.run()

if __name__ == "__main__":
    main()
