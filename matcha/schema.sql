
DROP TABLE IF EXISTS user;

CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	email TEXT NOT NULL,
	last_name TEXT NOT NULL,
	first_name TEXT NOT NULL,
	gender TEXT,
	age INTEGER,
	sexual_pref TEXT,
	biography TEXT,
	interest_tags TEXT,
	registered_on DATETIME NOT NULL,
	admin BOOLEAN NOT NULL DEFAULT FALSE,
	confirmed BOOLEAN NOT NULL DEFAULT FALSE,
);
