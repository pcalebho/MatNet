create table materials(
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    mat_name text, 
    tensile_strength int);

insert into materials (mat_name, ultimate_strength) values 
    {'AISI 4140 Steel, normalized at 870°C (1600°F), air cooled, 13 mm (0.5 in.) round',
    1020};
