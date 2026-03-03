TARGETS=lab.db penguins.db survey.db

all: ${TARGETS}

lab.db: lab/create-db.sql
	@rm -f $@
	sqlite3 $@ < $<

penguins.db: penguins/create-db.sql penguins/penguins.csv
	@rm -f $@
	sqlite3 $@ < $<

survey.db: survey/create-db.py
	@rm -f $@
	python $< $@ 192837

clean:
	@rm -f ${TARGETS}
