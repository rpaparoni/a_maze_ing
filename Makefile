.PHONY: install run debug clean lint lint-strict

install:
	pip install flake8 mypy pytest

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache *.pyc *.pyo
	rm -rf *.egg-info dist build
	rm -f mazegen*.whl mazegen*.tar.gz
	rm -f maze.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
