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
	@echo   " $(CYAN)    ___        __  ___                     _             $(RESET)  "
	@echo   " $(CYAN)   /   |      /  |/  /___ _____  ___      ( )____  _____ $(RESET)  "
	@echo   " $(CYAN)  / /| |     / /|_/ / __ '/_  / / _ \     / / __ \/ __ '/ $(RESET)  "
	@echo   " $(CYAN) / ___ |    / /  / / /_/ / / /_/  __/    / / / / / /_/ /  $(RESET)  "
	@echo   " $(CYAN)/_/  |_|___/_/  /_/\__,_/ /___/\___/____/_/_/ /_/\__, /   $(RESET)  "
	@echo   " $(CYAN)       /_____/                    /_____/       /____/    $(RESET)  "

install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	@echo "$(CYAN)Creando caja de arena e instalando dependencias...$(RESET)"
	@python3 -m venv $(VENV) > /dev/null 2>&1 && \
	$(PIP) install --upgrade pip > /dev/null 2>&1 && \
	$(PIP) install -r requirements.txt > /dev/null 2>&1 & \
	pid=$$!; \
	printf "$(CYAN)[$(RESET)"; \
	while kill -0 $$pid 2>/dev/null; do \
		printf "$(GREEN)█$(RESET)"; \
		sleep 0.15; \
	done; \
	printf "$(CYAN)]$(RESET)\n"
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