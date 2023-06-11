create table materials(
    id int NOT NULL AUTO_INCREMENT, 
    mat_name text, 
    ultimate_strength int,
    PRIMARY KEY (id));

create table heat_treatments(
    mat_id int NOT NULL AUTO_INCREMENT,
    treatment text,
    PRIMARY KEY (mat_id));

insert into materials (mat_name, ultimate_strength) 
values ('AISI 4140 Steel, normalized at 870°C (1600°F), air cooled, 13 mm (0.5 in.) round', 1020);
