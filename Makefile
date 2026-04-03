
CYAN   = \033[1;36m
RESET	= \033[0;0m

all: banner run

run:
	@python3 src/a_maze_ing.py

banner:
	@echo   " $(CYAN)    ___        __  ___                     _             $(RESET)  "
	@echo   " $(CYAN)   /   |      /  |/  /___ _____  ___      ( )____  _____ $(RESET)  "
	@echo   " $(CYAN)  / /| |     / /|_/ / __ '/_  / / _ \     / / __ \/ __ '/ $(RESET)  "
	@echo   " $(CYAN) / ___ |    / /  / / /_/ / / /_/  __/    / / / / / /_/ /  $(RESET)  "
	@echo   " $(CYAN)/_/  |_|___/_/  /_/\__,_/ /___/\___/____/_/_/ /_/\__, /   $(RESET)  "
	@echo   " $(CYAN)       /_____/                    /_____/       /____/    $(RESET)  "