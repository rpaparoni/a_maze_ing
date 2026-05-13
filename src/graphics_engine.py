import sys, random
from mlx import Mlx
from typing import Dict, Any, List

class MazeWindow:
    def __init__(self, config: Dict[str, str], maze: Any) -> None:
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.player_r: int = 0  # Fila 0
        self.player_c: int = 0  # Columna 0
        self.exit_r: int = 14
        self.exit_c: int = 19
        
        # Guardamos el laberinto para poder consultarlo
        self.maze = maze
        self.width = int(config["WIDTH"]) * 50
        self.height = int(config["HEIGHT"]) * 50
        self.wall_color: int = 0xFFFFFF
        
        self.win = self.mlx.mlx_new_window(self.ptr, self.width, 
                                          self.height, "A-Maze-ing")
        
        # Creamos el lienzo invisible (Imagen)
        self.img = self.mlx.mlx_new_image(self.ptr, self.width, self.height)
        
        # Obtenemos los datos técnicos del lienzo para poder pintar píxeles
        # addr es la dirección de memoria donde vive la imagen
        result = self.mlx.mlx_get_data_addr(self.img)
        self.addr = result[0]
        self.bpp = result[1]
        self.line_len = result[2]
        self.endian = result[3]

        # Ponemos los ganchos de teclado y cierre
        self.mlx.mlx_key_hook(self.win, self.handle_keypress, None)
        self.mlx.mlx_hook(self.win, 33, 0, self.handle_close, None)

    def put_pixel(self, x: int, y: int, color: int) -> None:
        # Calculamos la posición exacta del píxel en la memoria
        # Formula: y * longitud_linea + x * (bits_por_pixel / 8)
        offset = y * self.line_len + x * (self.bpp // 8)
        
        # Pintamos los canales de color (Azul, Verde, Rojo, Alpha)
        self.addr[offset] = color & 0xFF
        self.addr[offset + 1] = (color >> 8) & 0xFF
        self.addr[offset + 2] = (color >> 16) & 0xFF
        self.addr[offset + 3] = 0xFF

    def draw_rect(self, start_x: int, start_y: int, width: int, height: int, color: int) -> None:
        # Nuestra brocha universal para pintar lineas gruesas o bloques
        y: int = 0
        while y < height:
            x: int = 0
            while x < width:
                self.put_pixel(start_x + x, start_y + y, color)
                x += 1
            y += 1

    def draw_cell(self, row: int, col: int, walls: Dict[str, int]) -> None:
        # Coordenadas base del bloque en el lienzo (50 pixeles por celda)
        x0: int = col * 50
        y0: int = row * 50
        
        # 1. Pintamos el suelo de negro para borrar el gris
        self.draw_rect(x0, y0, 50, 50, 0x000000)
        
        # 2. Grosor y color de la pared (blanco)
        thick: int = 5
        # ¡Usamos el color actual del bote!
        color_wall: int = self.wall_color
        
        # 3. Levantamos las paredes si siguen en pie (si valen 1)
        if walls["north"] == 1:
            # Linea arriba
            self.draw_rect(x0, y0, 50, thick, color_wall)
            
        if walls["south"] == 1:
            # Linea abajo (y + 45 para que quede al borde)
            self.draw_rect(x0, y0 + 45, 50, thick, color_wall)
            
        if walls["east"] == 1:
            # Linea derecha (x + 45)
            self.draw_rect(x0 + 45, y0, thick, 50, color_wall)
            
        if walls["west"] == 1:
            # Linea izquierda
            self.draw_rect(x0, y0, thick, 50, color_wall)

    def draw_player(self) -> None:
        # Multiplicamos por 50 para ir a la celda correcta, 
        # y sumamos 10 para que quede en el centro
        x_pixel: int = (self.player_c * 50) + 10
        y_pixel: int = (self.player_r * 50) + 10
        
        # Un cuadrado verde radiactivo de 30x30
        self.draw_rect(x_pixel, y_pixel, 30, 30, 0x00FF00)

    def draw_exit(self) -> None:
        # Multiplicamos por 50 para ir a la celda correcta, 
        # y sumamos 10 para que quede en el centro
        x_pixel: int = (self.exit_c * 50) + 10
        y_pixel: int = (self.exit_r * 50) + 10
        
        # Un cuadrado rosa :P radiactivo de 30x30
        self.draw_rect(x_pixel, y_pixel, 30, 30, 0xFF00FF)

    def move_player(self, move_r: int, move_c: int, direction: str) -> None:
        # 1. Buscamos la celda en la que el jugador está parado AHORA mismo
        current_cell = self.maze.cells[(self.player_r, self.player_c)]
        
        # 2. ¡El sistema anti-fantasmas!
        # Le preguntamos a la celda: "¿Tu pared en esta dirección vale 1?"
        if current_cell.walls[direction] == 1:
            # Si hay pared, hacemos un 'return' vacío. 
            # Esto cancela la función inmediatamente y el jugador no se mueve.
            return
            
        # --- Si Python llega a esta línea, significa que NO hay pared ---
        
        # 3. "Borramos" al jugador de la celda vieja
        self.draw_cell(self.player_r, self.player_c, current_cell.walls)
        
        # 4. Actualizamos las coordenadas
        self.player_r += move_r
        self.player_c += move_c
        
        # 5. Dibujamos al jugador en la nueva posición
        self.draw_player()
        
        # 6. Pegamos la actualización en la ventana
        self.mlx.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)
        # Calculamos dinámicamente cuál es la meta
        goal_c = (self.width // 50) - 1
        goal_r = (self.height // 50) - 1

        # Comparamos nuestra posición con la meta
        if self.player_c == goal_c and self.player_r == goal_r:
            print("¡BINGO! ¡Laberinto completado!")
            self.clean_exit()

    def change_maze_color(self) -> None:
        # Una pequeña paleta de colores molones (Azul, Amarillo, Cian, Magenta, Naranja, Verde)
        colors = [
            0x0000FF,
            0xFFFF00,
            0x00FFFF,
            0xFF00FF,
            0xFFA500,
            0x800080,
            0x8B0000,
            0x006400,
            0x00008B,
            0x90EE90,
            0xADFF2F,
            0x9ACD32,
            0xFFFFFF
        ]
        
        # Elegimos uno al azar
        self.wall_color = random.choice(colors)
        
        # Le decimos al pintor: "¡Vuelve a pintar todo el lienzo con el nuevo color!"
        self.render_all()

    def render_all(self) -> None:
        keys: List[Any] = list(self.maze.cells.keys())
        i: int = 0
        
        # Recorremos el laberinto y le pasamos al pintor las paredes de cada celda
        while i < len(keys):
            coord = keys[i]
            cell = self.maze.cells[coord]
            self.draw_cell(coord[0], coord[1], cell.walls)
            i += 1

        self.draw_player()
        self.draw_exit()
        # Pegamos el lienzo terminado en la ventana
        self.mlx.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)

    def handle_keypress(self, key: int, param: Any) -> None:
        if key == 65307:
            self.clean_exit()
        elif key == 52:
            self.change_maze_color()
        elif key == 119: # W (Arriba -> Norte)
            self.move_player(-1, 0, "north")
        elif key == 115: # S (Abajo -> Sur)
            self.move_player(1, 0, "south")
        elif key == 97:  # A (Izquierda -> Oeste)
            self.move_player(0, -1, "west")
        elif key == 100: # D (Derecha -> Este)
            self.move_player(0, 1, "east")
            
    def handle_close(self, param: Any) -> None:
        self.clean_exit()

    def clean_exit(self) -> None:
        self.mlx.mlx_destroy_window(self.ptr, self.win)
        self.mlx.mlx_release(self.ptr)
        sys.exit(0)
        
    def run(self) -> None:
        # Pintamos antes de entrar en el bucle infinito
        self.render_all()
        self.mlx.mlx_loop(self.ptr)
