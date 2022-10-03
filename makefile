API_DIR = server
DB_DIR = db
REQ_DIR = .
LINTER = flake8

FORCE:

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin master

all_tests: lint_all unit

unit: FORCE
	cd $(API_DIR); pytest $(PYTESTFLAGS)

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt

docs: FORCE
	cd $(API_DIR); make docs
	cd $(DB_DIR); make docs

lint_all: FORCE
	$(LINTER)
