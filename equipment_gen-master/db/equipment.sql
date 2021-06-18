CREATE TABLE IF NOT EXISTS "cultures" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT UNIQUE,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO cultures VALUES(1,'Human','The human culture.  Very normal.  Memes and such');
INSERT INTO cultures VALUES(2,'Elvish','Pointy-eared tree-huggers');
INSERT INTO cultures VALUES(3,'Dwarvish','Stocky and rocky');
INSERT INTO cultures VALUES(4,'Goblin','Goblish');
INSERT INTO cultures VALUES(5,'Orcish','Gur');
CREATE TABLE IF NOT EXISTS "owners" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT UNIQUE,
	"description"	TEXT,
	"culture"	INTEGER,
	FOREIGN KEY("culture") REFERENCES "cultures"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO owners VALUES(1,'Mukqi','He''s Awesome','Human');
INSERT INTO owners VALUES(2,'Synsilon','Quite the elf of his time','Elvish');
INSERT INTO owners VALUES(4,'Buttars','The ultimate family name','Human');
CREATE TABLE IF NOT EXISTS "damage_types" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO damage_types VALUES(1,'slash','A cutting type of damage');
INSERT INTO damage_types VALUES(2,'pierce','Stabby stabby stabby');
INSERT INTO damage_types VALUES(3,'crush','Blunt force');
INSERT INTO damage_types VALUES(8,'asdf','adsfasdf');
CREATE TABLE IF NOT EXISTS "element_types" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"status_effect"	INTEGER,
	"description"	TEXT,
	FOREIGN KEY("status_effect") REFERENCES "status_effects"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO element_types VALUES(1,'fire',1,'Bright and Hot');
INSERT INTO element_types VALUES(2,'frost',2,NULL);
INSERT INTO element_types VALUES(3,'acid',3,NULL);
CREATE TABLE IF NOT EXISTS "status_effects" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"base_duration"	REAL,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO status_effects VALUES(1,'burn',3.0,'It''s HOT');
INSERT INTO status_effects VALUES(2,'freeze',NULL,NULL);
INSERT INTO status_effects VALUES(3,'bleed',NULL,NULL);
INSERT INTO status_effects VALUES(4,'corrode',NULL,NULL);
CREATE TABLE IF NOT EXISTS "unique" (
	"id"	INTEGER NOT NULL UNIQUE,
	"base_weapon"	INTEGER,
	"mod_hands"	INTEGER,
	"mod_damage_multiplier_min"	REAL,
	"mod_damage_multiplier_max"	REAL,
	"mod_damage_type_primary"	INTEGER,
	"mod_damage_type_secondary"	INTEGER,
	"level"	INTEGER,
	"mod_damage_elemental_type"	INTEGER,
	"damage_elemental_min"	INTEGER,
	"damage_elemental_max"	INTEGER,
	"mod_weight"	REAL,
	"mod_attacks_per_second"	REAL,
	"mod_hit_chance"	REAL,
	"culture"	INTEGER,
	"owner"	INTEGER
);
CREATE TABLE IF NOT EXISTS "base_weapons" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT UNIQUE,
	"hands"	INTEGER,
	"base_damage_min"	INTEGER,
	"base_damage_max"	INTEGER,
	"damage_type_primary"	INTEGER,
	"damage_type_secondary"	INTEGER,
	"base_weight"	REAL,
	"base_attacks_per_second"	REAL,
	"base_hit_chance"	REAL,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("damage_type_secondary") REFERENCES "damage_types"("id"),
	FOREIGN KEY("damage_type_primary") REFERENCES "damage_types"("id")
);
INSERT INTO base_weapons VALUES(2,'Axe',1,2,5,'slash','crush',12,7,0.9,'A simple hand axe');
INSERT INTO base_weapons VALUES(3,'Shortsword',1,2,6,'slash','pierce',12,2,1,'A simple short sword');
INSERT INTO base_weapons VALUES(5,'Mace',1,1,5,'crush','pierce',6.0,1.3,0.2,'asdf');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('cultures',5);
INSERT INTO sqlite_sequence VALUES('owners',4);
INSERT INTO sqlite_sequence VALUES('damage_types',8);
INSERT INTO sqlite_sequence VALUES('element_types',3);
INSERT INTO sqlite_sequence VALUES('status_effects',5);
INSERT INTO sqlite_sequence VALUES('base_weapons',5);
COMMIT;
