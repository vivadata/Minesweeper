

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
