import sys
from config_parser import parse_config
from graphics_engine import MazeWindow
from mazegen import MazeGenerator


def main() -> None:
    """Main function that initializes the program components."""
    if len(sys.argv) != 2:
        print("Error: Usage: python3 a_maze_ing.py config.txt")
        return

    # 1. Parsear el archivo de forma segura
    config_data = parse_config(sys.argv[1])
    if not config_data:
        return

    width = int(config_data["WIDTH"])
    height = int(config_data["HEIGHT"])
    entry_cords = config_data["ENTRY"].split(',')
    exit_cords = config_data["EXIT"].split(',')

    # Extraer variables para el inicio de la generacion
    start_c = int(entry_cords[0])
    start_r = int(entry_cords[1])
    exit_c = int(exit_cords[0])
    exit_r = int(exit_cords[1])

    # 2. Generar laberinto
    maze = MazeGenerator(height, width)
    maze.create_empty_grid()

    print(f"Grid initialized with {len(maze.cells)} cells.")

    # ¡El bloqueo del 42 recuperado!
    # Solo se dibuja si el mapa es lo bastante grande para que quepa
    if width > 8 and height > 6:
        maze.draw_fortytwo(start_r, start_c, exit_r, exit_c)
    else:
        print("error too small for 42")

    maze.carve_passages(start_r, start_c)
    maze.calculate_hex_for_all()

    # 3. Cumplir el requisito del PDF: Guardar el output
    output_filename = config_data["OUTPUT_FILE"]
    maze.save_to_file(output_filename, config_data)

    # 4. Iniciar graficos
    print("\n--- CONTROLS ---")
    print("[W, A, S, D] -> Move Player")
    print("[1] -> Regenerate Maze")
    print("[2] -> Show/Hide Solution Path")
    print("[3] -> Change Color")
    print("[4] -> Exit")

    game = MazeWindow(config_data, maze)
    game.run()


if __name__ == "__main__":
    main()
