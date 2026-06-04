import sys
import random
from mlx import Mlx
from typing import Dict
from typing import Any
from typing import List


class MazeWindow:
    """Manages the graphic rendering and keyboard events of the game."""
    def __init__(self, config: Dict[str, str], maze: Any) -> None:
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()

        # Ajustamos inicio y fin leyendo el config
        entry_cords: List[str] = config["ENTRY"].split(',')
        goal_cords: List[str] = config["EXIT"].split(',')

        self.player_c: int = int(entry_cords[0])
        self.player_r: int = int(entry_cords[1])

        self.start_c: int = self.player_c
        self.start_r: int = self.player_r

        self.exit_c: int = int(goal_cords[0])
        self.exit_r: int = int(goal_cords[1])

        self.maze = maze
        self.width = int(config["WIDTH"]) * 50
        self.height = int(config["HEIGHT"]) * 50
        self.wall_color: int = 0xFFFFFF
        self.show_solution: bool = False

        self.win = self.mlx.mlx_new_window(self.ptr, self.width, self.height, "A-Maze-ing")
        self.img = self.mlx.mlx_new_image(self.ptr, self.width, self.height)

        result = self.mlx.mlx_get_data_addr(self.img)
        self.addr = result[0]
        self.bpp = result[1]
        self.line_len = result[2]
        self.endian = result[3]

        self.mlx.mlx_key_hook(self.win, self.handle_keypress, None)
        self.mlx.mlx_hook(self.win, 33, 0, self.handle_close, None)

    def put_pixel(self, x: int, y: int, color: int) -> None:
        """Puts a single pixel in the memory buffer."""
        offset = y * self.line_len + x * (self.bpp // 8)
        self.addr[offset] = color & 0xFF
        self.addr[offset + 1] = (color >> 8) & 0xFF
        self.addr[offset + 2] = (color >> 16) & 0xFF
        self.addr[offset + 3] = 0xFF

    def draw_rect(self, start_x: int, start_y: int, width: int, height: int, color: int) -> None:
        """Draws a solid rectangle on the image."""
        y: int = 0
        while y < height:
            x: int = 0
            while x < width:
                self.put_pixel(start_x + x, start_y + y, color)
                x += 1
            y += 1

    def draw_cell(self, row: int, col: int, walls: Dict[str, int]) -> None:
        """Draws a single cell and its active walls."""
        x0: int = col * 50
        y0: int = row * 50

        self.draw_rect(x0, y0, 50, 50, 0x000000)
        thick: int = 5
        color_wall: int = self.wall_color

        if walls["north"] == 1:
            self.draw_rect(x0, y0, 50, thick, color_wall)
        if walls["south"] == 1:
            self.draw_rect(x0, y0 + 45, 50, thick, color_wall)
        if walls["east"] == 1:
            self.draw_rect(x0 + 45, y0, thick, 50, color_wall)
        if walls["west"] == 1:
            self.draw_rect(x0, y0, thick, 50, color_wall)

    def draw_player(self) -> None:
        """Draws the player square."""
        x_pixel: int = (self.player_c * 50) + 10
        y_pixel: int = (self.player_r * 50) + 10
        self.draw_rect(x_pixel, y_pixel, 30, 30, 0x00FF00)

    def draw_exit(self) -> None:
        """Draws the exit square."""
        x_pixel: int = (self.exit_c * 50) + 10
        y_pixel: int = (self.exit_r * 50) + 10
        self.draw_rect(x_pixel, y_pixel, 30, 30, 0xFF00FF)

    def draw_path(self) -> None:
        """Draws the solution path on the maze."""
        if not self.show_solution:
            return

        path = self.maze.find_path(self.player_r, self.player_c, self.exit_r, self.exit_c)
        i: int = 0
        while i < len(path):
            r = path[i][0]
            c = path[i][1]
            x_pixel: int = (c * 50) + 20
            y_pixel: int = (r * 50) + 20
            self.draw_rect(x_pixel, y_pixel, 10, 10, 0x00BFFF)
            i += 1

    def move_player(self, move_r: int, move_c: int, direction: str) -> None:
        """Handles player movement and collision."""
        current_cell = self.maze.cells[(self.player_r, self.player_c)]

        if current_cell.walls[direction] == 1:
            return

        self.draw_cell(self.player_r, self.player_c, current_cell.walls)

        self.player_r += move_r
        self.player_c += move_c

        # Volvemos a pintar cosas en el orden correcto
        if self.show_solution:
            self.draw_path()

        self.draw_exit()
        self.draw_player()

        self.mlx.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)

        if self.player_c == self.exit_c and self.player_r == self.exit_r:
            print("BINGO! Maze completed!")
            self.clean_exit()

    def change_maze_color(self) -> None:
        """Changes the wall color to a random one."""
        colors = [0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xFFA500, 0x800080, 0x90EE90, 0xFFFFFF]
        self.wall_color = random.choice(colors)
        self.render_all()

    def toggle_path(self) -> None:
        """Turns the solution path visibility on and off."""
        if self.show_solution:
            self.show_solution = False
        else:
            self.show_solution = True
        self.render_all()

    def regenerate_maze(self) -> None:
        """Creates a completely new maze and restarts the game."""
        print("Regenerating maze...")
        self.maze.create_empty_grid()
        if self.width > 10 and self.height > 10:
            self.maze.draw_fortytwo(self.start_r, self.start_c, self.exit_r, self.exit_c)
        self.maze.carve_passages(self.start_r, self.start_c)
        self.maze.calculate_hex_for_all()

        # Reset player to start
        self.player_c = self.start_c
        self.player_r = self.start_r
        self.show_solution = False

        self.render_all()

    def render_all(self) -> None:
        """Redraws the entire frame."""
        keys: List[Any] = list(self.maze.cells.keys())
        i: int = 0
        while i < len(keys):
            coord = keys[i]
            cell = self.maze.cells[coord]
            self.draw_cell(coord[0], coord[1], cell.walls)
            i += 1

        if self.show_solution:
            self.draw_path()

        self.draw_exit()
        self.draw_player()
        self.mlx.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)

    def handle_keypress(self, key: int, param: Any) -> None:
        """Maps keyboard inputs to game actions."""
        # 1, 2, 3, 4 menus
        if key == 49:    # '1'
            self.regenerate_maze()
        elif key == 50:  # '2'
            self.toggle_path()
        elif key == 51:  # '3'
            self.change_maze_color()
        elif key == 52 or key == 65307:  # '4' or ESC
            self.clean_exit()

        # W, A, S, D player movement
        elif key == 119:
            self.move_player(-1, 0, "north")
        elif key == 115:
            self.move_player(1, 0, "south")
        elif key == 97:
            self.move_player(0, -1, "west")
        elif key == 100:
            self.move_player(0, 1, "east")

    def handle_close(self, param: Any) -> None:
        self.clean_exit()

    def clean_exit(self) -> None:
        """Stops the MLX loop safely."""
        # En lugar de matar el programa, le decimos al bucle de C que termine.
        self.mlx.mlx_loop_exit(self.ptr)

    def run(self) -> None:
        """Starts the MLX loop and cleans up memory after it finishes."""
        self.render_all()

        # El programa se queda atrapado en esta linea mientras juegas
        self.mlx.mlx_loop(self.ptr)

        # --- Cuando llamas a clean_exit(), el bucle de arriba se rompe ---
        # --- y Python continua leyendo por aqui, cerrando todo limpiamente ---

        self.mlx.mlx_destroy_image(self.ptr, self.img)
        self.mlx.mlx_destroy_window(self.ptr, self.win)
        self.mlx.mlx_release(self.ptr)
