

all : tests format lint

.PHONY: tests
tests :
	@echo "Running tests..."
	export PYTHONPATH=.  ;\
	echo $(PYTHONPATH) ;\
	pytest -v 

.PHONY: lint
lint :
	@echo "Running lint..."
	pylint --rcfile=.pylintrc src 

.PHONY : format
format :
	@echo "Running format..."
	black .
