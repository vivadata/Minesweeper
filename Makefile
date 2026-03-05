all : tests format lint


.PHONY : app
app :
	@echo "Running app..."
	python web/app.py

##########################################################################################################################

# Testing & Quality

##########################################################################################################################



.PHONY: tests
tests : export PYTHONPATH = .
tests :
	@echo "Running all tests..."
	pytest -v tests/

.PHONY: unit-tests
unit-tests : export PYTHONPATH = .
unit-tests :
	@echo "Running unit tests..."
	pytest -v tests/unit_tests/

.PHONY: functional-tests
functional-tests : export PYTHONPATH = .
functional-tests :
	@echo "Running functional tests..."
	pytest -v tests/functionnal_tests/

.PHONY: coverage
coverage : export PYTHONPATH = .
coverage :
	mkdir -p tests_result
	pytest -v --cov=src --cov=web --cov-config=.coveragerc \
		--cov-report=term-missing \
		--cov-report=xml:tests_result/coverage.xml \
		--cov-report=html:tests_result/htmlcov \
		--junitxml=tests_result/junit.xml \
		tests/


.PHONY: lint
lint :
	@echo "Running lint..."
	pylint --rcfile=.pylintrc src

.PHONY : format
format :
	@echo "Running format..."
	black .



########################################################################################################################

# Setup the virtual environment

########################################################################################################################

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
	pip install --upgrade pip
	pip install -r requirements.txt
