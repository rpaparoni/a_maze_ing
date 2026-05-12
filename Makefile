CYAN = \\033[1;36m
RESET = \\033[0;0m
RED = \\033[0;31m
GREEN = \\033[0;32m

# Configuración del entorno
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Archivos principales
MAIN = src/a_maze_ing.py
CONFIG = config.txt

all: banner install

banner:
	@echo "$(CYAN)======================================"
	@echo "           A-MAZE-ING                "
	@echo "======================================$(RESET)"

install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	@echo "$(CYAN)Creando caja de arena (venv)...$(RESET)"
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@touch $(VENV)/bin/activate
	@echo "$(GREEN)¡Entorno listo!$(RESET)"

run: install
	@echo "$(CYAN)Arrancando el laberinto...$(RESET)"
	@$(PYTHON) $(MAIN) $(CONFIG)

# REGLAS DE LIMPIEZA (Lo que pediste)

# 1. Clean: Borra solo la basura temporal del código
clean:
	@echo "$(RED)Borrando archivos temporales (__pycache__, etc.)...$(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf .mypy_cache .pytest_cache

# 2. Fclean: Limpieza total (Borra la basura + el entorno virtual + el laberinto generado)
fclean: clean
	@echo "$(RED)Borrando entorno virtual y archivos de salida...$(RESET)"
	@rm -rf $(VENV)
	@rm -f maze.txt  # Asumiendo que este es tu archivo de salida predeterminado

# 3. Re: El botón de pánico. Borra todo y lo vuelve a instalar de cero
re: fclean all

.PHONY: all banner install run clean fclean re