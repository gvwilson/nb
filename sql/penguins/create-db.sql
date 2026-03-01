-- Create table.
create table penguins (
    species text,
    island text,
    bill_length_mm real,
    bill_depth_mm real,
    flipper_length_mm real,
    body_mass_g real,
    sex text
);

-- Import data.
.mode csv
.import penguins.csv penguins

-- Replace empty strings with nulls.
update penguins set bill_length_mm = null where bill_length_mm = '';
update penguins set bill_depth_mm = null where bill_depth_mm = '';
update penguins set flipper_length_mm = null where flipper_length_mm = '';
update penguins set body_mass_g = null where body_mass_g = '';
update penguins set sex = null where sex = '';
