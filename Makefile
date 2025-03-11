all : tests format lint

.PHONY: tests
tests : export PYTHONPATH = .
tests :
	@echo "Running tests..."
	pytest -v

.PHONY: lint
lint :
	@echo "Running lint..."
	pylint --rcfile=.pylintrc src

.PHONY : format
format :
	@echo "Running format..."
	black .

.PHONY : app
app :
	@echo "Running app..."


########################################################################################################################

# Setup the virtual environment
.PHONY : setup

activate :
	@if ! pyenv virtualenvs | grep -q minesweeper; then \
		echo "Creating virtualenv..."; \
		pyenv virtualenv minesweeper; \
	else \
		echo "Virtualenv already exists"; \
	fi
	pyenv local minesweeper

install : activate
	@echo "Installing dependencies..."
	pip install -r requirements.txt
