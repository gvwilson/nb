TARGETS=penguins.db survey.db

all: ${TARGETS}

penguins.db: penguins/create-db.sql penguins/penguins.csv
	@rm -f $@
	sqlite3 $@ < $<

survey.db: survey/create-db.py
	@rm -f $@
	python $< $@ 192837

clean:
	@rm -f ${TARGETS}
