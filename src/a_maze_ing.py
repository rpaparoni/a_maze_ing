import sys
from config_parser import parse_config
from graphics_engine import MazeWindow


def main() -> None:
    # Comprobamos que el usuario nos pase el archivo de configuración
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    # 1. Leemos los datos
    config_data = parse_config(sys.argv[1])
    
    # 2. Si los datos están incompletos, no seguimos
    if not config_data:
        return

    # 3. Creamos e iniciamos la interfaz gráfica
    game = MazeWindow(config_data)
    game.run()


if __name__ == "__main__":
    main()
