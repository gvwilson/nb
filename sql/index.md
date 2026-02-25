# Core Features

## Selecting Constant

```sql
select 1;
```
```txt
1
```

-   `select` is a keyword
-   Normally used to select data from table…
-   …but if all we want is a constant value, we don't need to specify one
-   Semi-colon terminator is required

## Selecting All Values from Table

```sql
select * from penguins;
```
```txt
Gentoo|Biscoe|51.3|14.2|218.0|5300.0|MALE
Adelie|Dream|35.7|18.0|202.0|3550.0|FEMALE
Adelie|Torgersen|36.6|17.8|185.0|3700.0|FEMALE
Chinstrap|Dream|55.8|19.8|207.0|4000.0|MALE
Adelie|Dream|38.1|18.6|190.0|3700.0|FEMALE
Adelie|Dream|36.2|17.3|187.0|3300.0|FEMALE
Adelie|Dream|39.5|17.8|188.0|3300.0|FEMALE
Gentoo|Biscoe|42.6|13.7|213.0|4950.0|FEMALE
Gentoo|Biscoe|52.1|17.0|230.0|5550.0|MALE
Adelie|Torgersen|36.7|18.8|187.0|3800.0|FEMALE
```

-   An actual [query](g:query)
-   Use `*` to mean "all columns"
-   Use <code>from <em>tablename</em></code> to specify table
-   Output format is not particularly readable

## Specifying Columns

```sql
select
    species,
    island,
    sex
from penguins;
```
```txt
|  species  |  island   |  sex   |
|-----------|-----------|--------|
| Gentoo    | Biscoe    | MALE   |
| Adelie    | Dream     | FEMALE |
| Adelie    | Torgersen | FEMALE |
| Chinstrap | Dream     | MALE   |
| Adelie    | Dream     | FEMALE |
| Adelie    | Dream     | FEMALE |
| Adelie    | Dream     | FEMALE |
| Gentoo    | Biscoe    | FEMALE |
| Gentoo    | Biscoe    | MALE   |
| Adelie    | Torgersen | FEMALE |
```

-   Specify column names separated by commas
    -   In any order
    -   Duplicates allowed
-   Line breaks encouraged for readability

## Sorting

```sql
select
    species,
    sex,
    island
from penguins
order by island asc, sex desc;
```
```txt
|  species  |  sex   |  island   |
|-----------|--------|-----------|
| Gentoo    | MALE   | Biscoe    |
| Gentoo    | MALE   | Biscoe    |
| Gentoo    | FEMALE | Biscoe    |
| Chinstrap | MALE   | Dream     |
| Adelie    | FEMALE | Dream     |
| Adelie    | FEMALE | Dream     |
| Adelie    | FEMALE | Dream     |
| Adelie    | FEMALE | Dream     |
| Adelie    | FEMALE | Torgersen |
| Adelie    | FEMALE | Torgersen |
```

-   `order by` must follow `from` (which must follow `select`)
-   `asc` is ascending, `desc` is descending
    -   Default is ascending, but please specify

## Exercise

Write a SQL query to select the sex and body mass columns from the `penguins` in that order,
sorted such that the largest body mass appears first.

## Limiting Output

-   Full dataset has 344 rows

```sql
select
    species,
    sex,
    island
from penguins
order by species, sex, island
limit 10;
```
```txt
| species |  sex   |  island   |
|---------|--------|-----------|
| Adelie  |        | Dream     |
| Adelie  |        | Torgersen |
| Adelie  |        | Torgersen |
| Adelie  |        | Torgersen |
| Adelie  |        | Torgersen |
| Adelie  |        | Torgersen |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
```

-   Comments start with `--` and run to the end of the line
-   <code>limit <em>N</em></code> specifies maximum number of rows returned by query

## Paging Output

```sql
select
    species,
    sex,
    island
from penguins
order by species, sex, island
limit 10 offset 3;
```
```txt
| species |  sex   |  island   |
|---------|--------|-----------|
| Adelie  |        | Torgersen |
| Adelie  |        | Torgersen |
| Adelie  |        | Torgersen |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
| Adelie  | FEMALE | Biscoe    |
```

-   <code>offset <em>N</em></code> must follow `limit`
-   Specifies number of rows to skip from the start of the selection
-   So this query skips the first 3 and shows the next 10

## Removing Duplicates

```sql
select distinct
    species,
    sex,
    island
from penguins;
```
```txt
|  species  |  sex   |  island   |
|-----------|--------|-----------|
| Adelie    | MALE   | Torgersen |
| Adelie    | FEMALE | Torgersen |
| Adelie    |        | Torgersen |
| Adelie    | FEMALE | Biscoe    |
| Adelie    | MALE   | Biscoe    |
| Adelie    | FEMALE | Dream     |
| Adelie    | MALE   | Dream     |
| Adelie    |        | Dream     |
| Chinstrap | FEMALE | Dream     |
| Chinstrap | MALE   | Dream     |
| Gentoo    | FEMALE | Biscoe    |
| Gentoo    | MALE   | Biscoe    |
| Gentoo    |        | Biscoe    |
```

-   `distinct` keyword must appear right after `select`
    -   SQL was supposed to read like English
-   Shows distinct combinations
-   Blanks in `sex` column show missing data
    -   We'll talk about this in a bit

## Exercise

1.  Write a SQL query to select the islands and species
    from rows 50 to 60 inclusive of the `penguins` table.
    Your result should have 11 rows.

2.  Modify your query to select distinct combinations of island and species
    from the same rows
    and compare the result to what you got in part 1.

## Filtering Results

```sql
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe';
```
```txt
| species |  sex   | island |
|---------|--------|--------|
| Adelie  | FEMALE | Biscoe |
| Adelie  | MALE   | Biscoe |
| Gentoo  | FEMALE | Biscoe |
| Gentoo  | MALE   | Biscoe |
| Gentoo  |        | Biscoe |
```

-   <code>where <em>condition</em></code> [filters](g:filter) the rows produced by selection
-   Condition is evaluated independently for each row
-   Only rows that pass the test appear in results
-   Use single quotes for `'text data'` and double quotes for `"weird column names"`
    -   SQLite will accept double-quoted text data but [SQLFluff][sqlfluff] will complain

## Exercise

1.  Write a query to select the body masses from `penguins` that are less than 3000.0 grams.

2.  Write another query to select the species and sex of penguins that weight less than 3000.0 grams.
    This shows that the columns displayed and those used in filtering are independent of each other.

## Filtering with More Complex Conditions

```sql
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe' and sex != 'MALE';
```
```txt
| species |  sex   | island |
|---------|--------|--------|
| Adelie  | FEMALE | Biscoe |
| Gentoo  | FEMALE | Biscoe |
```

-   `and`: both sub-conditions must be true
-   `or`: either or both part must be true
-   Notice that the row for Gentoo penguins on Biscoe island with unknown (empty) sex didn't pass the test
    -   We'll talk about this in a bit

## Exercise

1.  Use the `not` operator to select penguins that are *not* Gentoos.

2.  SQL's `or` is an [inclusive or](g:inclusive_or):
    it succeeds if either *or both* conditions are true.
    SQL does not provide a specific operator for [exclusive or](g:exclusive_or),
    which is true if either *but not both* conditions are true,
    but the same effect can be achieved using `and`, `or`, and `not`.
    Write a query to select penguins that are female *or* on Torgersen Island *but not both*.

## Doing Calculations

```sql
select
    flipper_length_mm / 10.0,
    body_mass_g / 1000.0
from penguins
limit 3;
```
```txt
| flipper_length_mm / 10.0 | body_mass_g / 1000.0 |
|--------------------------|----------------------|
| 18.1                     | 3.75                 |
| 18.6                     | 3.8                  |
| 19.5                     | 3.25                 |
```

-   Can do the usual kinds of arithmetic on individual values
    -   Calculation done for each row independently
-   Column name shows the calculation done

## Renaming Columns

```sql
select
    flipper_length_mm / 10.0 as flipper_cm,
    body_mass_g / 1000.0 as weight_kg,
    island as where_found
from penguins
limit 3;
```
```txt
| flipper_cm | weight_kg | where_found |
|------------|-----------|-------------|
| 18.1       | 3.75      | Torgersen   |
| 18.6       | 3.8       | Torgersen   |
| 19.5       | 3.25      | Torgersen   |
```

-   Use <code><em>expression</em> as <em>name</em></code> to rename
-   Give result of calculation a meaningful name
-   Can also rename columns without modifying

## Exercise

Write a single query that calculates and returns:

1.  A column called `what_where` that has the species and island of each penguin
    separated by a single space.
2.  A column called `bill_ratio` that has the ratio of bill length to bill depth.

You can use the `||` operator to concatenate text to solve part 1,
or look at [the documentation for SQLite's `format()` function][sqlite_format].

## Checking Understanding

<figure id="f:core_select_concept_map">
  <img src="core_select_concept_map.svg" alt="box and arrow diagram of concepts related to selection"/>
  <figcaption>Selection Concepts</figcaption>
</figure>
