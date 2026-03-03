SCENARIOS_SRC=$(wildcard *.py)
SCENARIOS_TXT=$(patsubst %.py,output/%.txt,${SCENARIOS_SRC})
SCENARIOS_GRAPH=$(patsubst %.py,output/%.html,${SCENARIOS_SRC})

all: commands

## commands: show available commands (*)
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## scenarios: regenerate scenario output
scenarios: ${SCENARIOS_TXT} ${SCENARIOS_GRAPH}

output/%.txt output/%.html: %.py
	@mkdir -p output
	python $< output/$*.html > output/$*.txt
