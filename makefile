.PHONY: setup
setup: packages

.PHONY: packages
packages:
	pipenv lock && pipenv install --system --deploy --ignore-pipfile
	
.PHONY: unsed
unsed:
	autoflake --in-place --remove-unused-variables tests/*.py app/*.py

.PHONY: format
format: unsed clean
	autopep8 --in-place --aggressive --aggressive tests/*.py app/*.py

.PHONY: test
test:
	pytest tests/

.PHONY: clean-pyc clean-build clean
clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.egg

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +