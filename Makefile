.PHONY: docs
all: commands

MARIMO := uv run marimo

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## site: build GitHub pages site
site:
	@mkdir -p docs
	@cp pages/index.html docs/
	@cp pages/neat.css docs/
	${MARIMO} export html-wasm --force --mode edit --sandbox turtle/turtle.py -o docs/turtle.html

## serve: serve website
serve:
	python -m http.server --directory docs

## check: check Python code issues
check:
	@ruff check .

## clean: clean up
clean:
	@rm -rf ./dist ./src/faw/static
	@find . -path './.venv' -prune -o -type d -name '__pycache__' -exec rm -rf {} +
	@find . -path './.venv' -prune -o -type f -name '*~' -exec rm {} +

## fix: fix formatting and code issues
fix:
	@ruff format .
	@ruff check --fix .
