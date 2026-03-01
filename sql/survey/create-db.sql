-- Create database to be used for learners.
-- The data for the database are available as CSV files.
-- For more information, see https://www.sqlite.org/cli.html#csv

-- Generate tables.
create table person (id text, personal text, family text);
create table site (name text, lat real, long real);
create table visited (id text, site text, dated text);
create table survey (taken integer, person text, quant text, reading real);

-- Import data.
.mode csv
.import person.csv person
.import site.csv site
.import survey.csv survey
.import visited.csv visited

-- Convert empty strings to NULLs.
UPDATE visited SET dated = null WHERE dated = '';
UPDATE survey SET person = null WHERE person = '';
