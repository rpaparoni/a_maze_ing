from typing import Dict, Tuple, List
import random

class Cell:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.is_42: bool = False
        
        # 1 significa pared cerrada, 0 significará pared rota
        self.walls: Dict[str, int] = {
            "north": 1,
            "south": 1,
            "east": 1,
            "west": 1
        }
        
        # Esta es la marca para nuestro "topo". 
        # Si es False, significa que es tierra virgen.
        self.visited: bool = False
        self.hex_value: str = "F"  # <-- codigo hexadecimal por defecto, "todo esta cerrardo"


class MazeGenerator:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        
        # Aquí guardaremos el mapa. 
        # La clave será la coordenada (ej: (0, 1)) y el valor será la Celda.
        self.cells: Dict[Tuple[int, int], Cell] = {}

    def create_empty_grid(self) -> None:
        row: int = 0
        
        # Nuestro bucle para las filas
        while row < self.height:
            col: int = 0
            
            # Nuestro bucle para las columnas
            while col < self.width:
                # Fabricamos una celda nueva
                new_cell = Cell(row, col)
                
                # La guardamos en el diccionario usando su posición como llave
                self.cells[(row, col)] = new_cell
                
                col += 1
            row += 1
        
    def get_unvisited_neighbors(self, row: int, col: int) -> List[Tuple[str, int, int]]:
        # El radar del topo: busca celdas vecinas que tengan visited == False
        neighbors: List[Tuple[str, int, int]] = []
        
        # Miramos al Norte (arriba)
        if row > 0 and self.cells[(row - 1, col)].visited == False:
            neighbors.append(("north", row - 1, col))
            
        # Miramos al Sur (abajo)
        if row < self.height - 1 and self.cells[(row + 1, col)].visited == False:
            neighbors.append(("south", row + 1, col))
            
        # Miramos al Este (derecha)
        if col < self.width - 1 and self.cells[(row, col + 1)].visited == False:
            neighbors.append(("east", row, col + 1))
            
        # Miramos al Oeste (izquierda)
        if col > 0 and self.cells[(row, col - 1)].visited == False:
            neighbors.append(("west", row, col - 1))
            
        return neighbors

    def carve_passages(self, start_row: int, start_col: int) -> None:
        # El hilo atado a la cintura del topo
        stack: List[Tuple[int, int]] = []
        
        # El topo pisa la primera casilla
        self.cells[(start_row, start_col)].visited = True
        stack.append((start_row, start_col))
        
        # Mientras el topo tenga hilo (casillas a las que retroceder)
        while len(stack) > 0:
            # Miramos dónde está parado el topo actualmente (la última casilla de la lista)
            current = stack[-1]
            curr_row = current[0]
            curr_col = current[1]
            
            # Encendemos el radar
            neighbors = self.get_unvisited_neighbors(curr_row, curr_col)
            
            if len(neighbors) > 0:
                # Si hay tierra virgen, elegimos una dirección al azar
                chosen = random.choice(neighbors)
                direction = chosen[0]
                next_row = chosen[1]
                next_col = chosen[2]
                
                # ¡ROMPEMOS LA PARED DE NUESTRA CELDA! (0 significa abierta)
                self.cells[(curr_row, curr_col)].walls[direction] = 0
                
                # ¡ROMPEMOS LA PARED DE LA CELDA VECINA! (Tiene que ser la pared opuesta)
                if direction == "north":
                    self.cells[(next_row, next_col)].walls["south"] = 0
                elif direction == "south":
                    self.cells[(next_row, next_col)].walls["north"] = 0
                elif direction == "east":
                    self.cells[(next_row, next_col)].walls["west"] = 0
                elif direction == "west":
                    self.cells[(next_row, next_col)].walls["east"] = 0
                    
                # El topo avanza: marca la nueva celda como visitada y suelta hilo (la añade)
                self.cells[(next_row, next_col)].visited = True
                stack.append((next_row, next_col))
            else:
                # Si está rodeado de túneles ya excavados, recoge hilo y retrocede
                stack.pop()
    
    def calculate_hex_for_all(self) -> None:
        # Nuestro diccionario de traducción
        hex_sequence: str = "0123456789ABCDEF"
        
        # Sacamos la lista de coordenadas para poder recorrerla
        keys: List[Tuple[int, int]] = list(self.cells.keys())
        i: int = 0
        
        while i < len(keys):
            coord = keys[i]
            cell = self.cells[coord]
            
            # Calculamos la suma de las paredes que siguen en pie (multiplicadas por su peso)
            valor: int = 0
            valor += cell.walls["north"] * 1
            valor += cell.walls["east"] * 2
            valor += cell.walls["south"] * 4
            valor += cell.walls["west"] * 8
            
            # Buscamos la letra en la secuencia y la guardamos
            cell.hex_value = hex_sequence[valor]
            
            i += 1
        
    def draw_fortytwo(self) -> None:
        # 1. Encontramos el centro matemático
        mid_r: int = self.height // 2
        mid_c: int = self.width // 2
        
        # 2. Lista de coordenadas relativas para formar el '4' y el '2'
        # (Basado en el diseño que usa la escuela)
        # Formato: (fila_relativa, columna_relativa)
        
        # Celdas para el "4"
        self.block_cell(mid_r, mid_c - 1)
        self.block_cell(mid_r, mid_c - 2)
        self.block_cell(mid_r, mid_c - 3)
        self.block_cell(mid_r - 1, mid_c - 3)
        self.block_cell(mid_r - 2, mid_c - 3)
        self.block_cell(mid_r + 1, mid_c - 1)
        self.block_cell(mid_r + 2, mid_c - 1)
        self.block_cell(mid_r - 1, mid_c - 1)
        self.block_cell(mid_r - 2, mid_c - 1)
        
        # Celdas para el "2"
        self.block_cell(mid_r, mid_c + 1)
        self.block_cell(mid_r, mid_c + 2)
        self.block_cell(mid_r, mid_c + 3)
        self.block_cell(mid_r - 1, mid_c + 3)
        self.block_cell(mid_r - 2, mid_c + 3)
        self.block_cell(mid_r - 2, mid_c + 2)
        self.block_cell(mid_r - 2, mid_c + 1)
        self.block_cell(mid_r + 1, mid_c + 1)
        self.block_cell(mid_r + 2, mid_c + 1)
        self.block_cell(mid_r + 2, mid_c + 2)
        self.block_cell(mid_r + 2, mid_c + 3)

    def block_cell(self, r: int, c: int) -> None:
        # Función auxiliar para marcar la celda y darle un color especial
        if (r, c) in self.cells:
            self.cells[(r, c)].visited = True
            # Le ponemos una marca especial para que el pintor sepa qué es
            self.cells[(r, c)].is_42 = True
