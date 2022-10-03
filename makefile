API_DIR = server
DB_DIR = db
REQ_DIR = .
LINTER = flake8
PYTESTFLAGS = -vv --verbose --tb=short


FORCE:

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin master

all_tests:
	cd $(API_DIR) && make tests
	cd $(DB_DIR) && make tests

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt

docs: FORCE
	cd $(API_DIR); make docs
	cd $(DB_DIR); make docs

lint_all: FORCE
	$(LINTER)
