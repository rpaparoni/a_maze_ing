import sys
from mlx import Mlx
from typing import Dict, Any

class MazeWindow:
    def __init__(self, config: Dict[str, str]) -> None:
        # Inicializamos la conexión con MiniLibX
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        
        # Calculamos el tamaño (Celdas * 50 píxeles por cada una)
        self.width = int(config["WIDTH"]) * 50
        self.height = int(config["HEIGHT"]) * 50
        
        # Creamos la ventana física
        self.win = self.mlx.mlx_new_window(self.ptr, self.width, 
                                          self.height, "A-Maze-ing")
        # 1. El gancho del teclado:
        # mlx_key_hook captura cualquier tecla y se la pasa a 'handle_keypress'
        self.mlx.mlx_key_hook(self.win, self.handle_keypress, None)
        
        # 2. El gancho de la ventana (La 'X' roja):
        # El número 33 es el código interno del sistema (X11) para "cerrar ventana"
        self.mlx.mlx_hook(self.win, 33, 0, self.handle_close, None)

        # Función que reacciona a las teclas
    def handle_keypress(self, key: int, param: Any) -> None:
        # En los sistemas Linux, el código de la tecla ESC es 65307
        if key == 65307:
            print("Closing gracefully with ESC...")
            self.clean_exit()
            
    # Función que reacciona a la 'X' de la ventana
    def handle_close(self, param: Any) -> None:
        print("Closing from the 'X' button...")
        self.clean_exit()

    # Función de limpieza (Norminette aprueba no repetir código)
    def clean_exit(self) -> None:
        # Rompemos la ventana
        self.mlx.mlx_destroy_window(self.ptr, self.win)
        # Liberamos la memoria principal del motor
        self.mlx.mlx_release(self.ptr)
        # Le decimos a Python que termine el programa sin errores (0)
        sys.exit(0)
        
    def run(self) -> None:
        # Dejamos la ventana abierta escuchando eventos
        self.mlx.mlx_loop(self.ptr)
