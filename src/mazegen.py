from typing import Dict, Tuple, List
import random


class Cell:
    """Represents a single cell inside the maze."""
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.is_42: bool = False
        self.walls: Dict[str, int] = {
            "north": 1,
            "south": 1,
            "east": 1,
            "west": 1
        }
        self.visited: bool = False
        self.hex_value: str = "F"


class MazeGenerator:
    """Handles the creation, logic, and solving of the perfect maze."""
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.cells: Dict[Tuple[int, int], Cell] = {}

    def create_empty_grid(self) -> None:
        """Initializes the grid with solid walls."""
        row: int = 0
        while row < self.height:
            col: int = 0
            while col < self.width:
                self.cells[(row, col)] = Cell(row, col)
                col += 1
            row += 1

    def get_unvisited_neighbors(self, row: int, col: int) -> List[Tuple[str, int, int]]:
        """Returns adjacent cells that haven't been visited yet."""
        neighbors: List[Tuple[str, int, int]] = []
        if row > 0 and self.cells[(row - 1, col)].visited == False:
            neighbors.append(("north", row - 1, col))
        if row < self.height - 1 and self.cells[(row + 1, col)].visited == False:
            neighbors.append(("south", row + 1, col))
        if col < self.width - 1 and self.cells[(row, col + 1)].visited == False:
            neighbors.append(("east", row, col + 1))
        if col > 0 and self.cells[(row, col - 1)].visited == False:
            neighbors.append(("west", row, col - 1))
        return neighbors

    def carve_passages(self, start_row: int, start_col: int) -> None:
        """Excavates the maze paths using a backtracking algorithm."""
        stack: List[Tuple[int, int]] = []
        self.cells[(start_row, start_col)].visited = True
        stack.append((start_row, start_col))

        while len(stack) > 0:
            current = stack[-1]
            curr_row = current[0]
            curr_col = current[1]
            neighbors = self.get_unvisited_neighbors(curr_row, curr_col)

            if len(neighbors) > 0:
                chosen = random.choice(neighbors)
                direction = chosen[0]
                next_row = chosen[1]
                next_col = chosen[2]

                self.cells[(curr_row, curr_col)].walls[direction] = 0
                if direction == "north":
                    self.cells[(next_row, next_col)].walls["south"] = 0
                elif direction == "south":
                    self.cells[(next_row, next_col)].walls["north"] = 0
                elif direction == "east":
                    self.cells[(next_row, next_col)].walls["west"] = 0
                elif direction == "west":
                    self.cells[(next_row, next_col)].walls["east"] = 0
       
                self.cells[(next_row, next_col)].visited = True
                stack.append((next_row, next_col))
            else:
                stack.pop()

    def calculate_hex_for_all(self) -> None:
        """Calculates the hexadecimal representation of each cell's walls."""
        hex_sequence: str = "0123456789ABCDEF"
        keys: List[Tuple[int, int]] = list(self.cells.keys())
        i: int = 0

        while i < len(keys):
            coord = keys[i]
            cell = self.cells[coord]
            valor: int = 0
            valor += cell.walls["north"] * 1
            valor += cell.walls["east"] * 2
            valor += cell.walls["south"] * 4
            valor += cell.walls["west"] * 8
            cell.hex_value = hex_sequence[valor]
            i += 1

    def save_to_file(self, filename: str) -> None:
        """Saves the generated maze to a text file in hexadecimal format."""
        try:
            f = open(filename, "w")
            row: int = 0
            while row < self.height:
                col: int = 0
                line: str = ""
                while col < self.width:
                    line += self.cells[(row, col)].hex_value
                    col += 1
                f.write(line + "\n")
                row += 1
            f.close()
            print(f"Maze successfully saved to {filename}")
        except Exception:
            print("Error: Could not save the maze to the output file.")

    def draw_fortytwo(self) -> None:
        """Marks the center cells to form the '42' logo before carving."""
        mid_r: int = self.height // 2
        mid_c: int = self.width // 2

        # Celdas para formar el numero "4"
        self.block_cell(mid_r, mid_c - 1)
        self.block_cell(mid_r, mid_c - 2)
        self.block_cell(mid_r, mid_c - 3)
        self.block_cell(mid_r - 1, mid_c - 3)
        self.block_cell(mid_r - 2, mid_c - 3)
        self.block_cell(mid_r + 1, mid_c - 1)
        self.block_cell(mid_r + 2, mid_c - 1)
        self.block_cell(mid_r - 1, mid_c - 1)
        self.block_cell(mid_r - 2, mid_c - 1)

        # Celdas para formar el numero "2"
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
        """Helper function to mark a cell as visited to block the topo."""
        if (r, c) in self.cells:
            # Al poner visited en True, el topo pensara que ya paso por ahi
            # y no destruira sus paredes, dejandolo como un bloque macizo
            self.cells[(r, c)].visited = True
            self.cells[(r, c)].is_42 = True

    def find_path(self, start_r: int, start_c: int, end_r: int, end_c: int) -> List[Tuple[int, int]]:
        """Finds the solution path from entry to exit using a BFS approach."""
        keys: List[Tuple[int, int]] = list(self.cells.keys())
        i: int = 0
        while i < len(keys):
            self.cells[keys[i]].visited = False
            i += 1
            
        stack: List[List[Tuple[int, int]]] = [[(start_r, start_c)]]
        self.cells[(start_r, start_c)].visited = True
        
        while len(stack) > 0:
            current_path = stack.pop()
            current_node = current_path[-1]
            r = current_node[0]
            c = current_node[1]
            
            if r == end_r and c == end_c:
                return current_path
                
            cell = self.cells[(r, c)]
            
            if cell.walls["north"] == 0 and not self.cells[(r-1, c)].visited:
                self.cells[(r-1, c)].visited = True
                new_path = list(current_path)
                new_path.append((r-1, c))
                stack.append(new_path)
                
            if cell.walls["south"] == 0 and not self.cells[(r+1, c)].visited:
                self.cells[(r+1, c)].visited = True
                new_path = list(current_path)
                new_path.append((r+1, c))
                stack.append(new_path)
                
            if cell.walls["east"] == 0 and not self.cells[(r, c+1)].visited:
                self.cells[(r, c+1)].visited = True
                new_path = list(current_path)
                new_path.append((r, c+1))
                stack.append(new_path)
                
            if cell.walls["west"] == 0 and not self.cells[(r, c-1)].visited:
                self.cells[(r, c-1)].visited = True
                new_path = list(current_path)
                new_path.append((r, c-1))
                stack.append(new_path)
                
        return []
