CREATE TABLE Player(
   name text NOT NULL,
   id text NOT NULL,
   PRIMARY KEY(id)
);

CREATE TABLE League(
   name text NOT NULL,
   PRIMARY KEY(name)
);

CREATE TABLE Format(
   name text NOT NULL,
   PRIMARY KEY(name)
);

CREATE TABLE Division(
   name text NOT NULL,
   PRIMARY KEY(name)
);

CREATE TABLE Team(
   name text NOT NULL,
   id int NOT NULL,
   PRIMARY KEY(id)
);

CREATE TABLE Class(
   name text NOT NULL,
   PRIMARY KEY(name)
);

CREATE TABLE PlaysOn(
   player text NOT NULL,
   team int NOT NULL, 
   FOREIGN KEY(player) REFERENCES Player(id),
   FOREIGN KEY(team) REFERENCES Team(id),
   PRIMARY KEY(player, team)
);

CREATE TABLE TeamFormat(
   team int NOT NULL,
   format text NOT NULL,
   FOREIGN KEY(team) REFERENCES team(id),
   FOREIGN KEY(format) REFERENCES format(name),
   PRIMARY KEY(team, format)
);

CREATE TABLE LeagueDivision(
   league text NOT NULL,
   division text NOT NULL,
   rank int NOT NULL,
   FOREIGN KEY(league) REFERENCES League(name),
   FOREIGN KEY(division) REFERENCES Division(name),
   PRIMARY KEY(league,division)
);

CREATE TABLE LeagueFormat(
   league text NOT NULL,
   format text NOT NULL,
   FOREIGN KEY(league) REFERENCES League(name),
   FOREIGN KEY(format) REFERENCES Format(name),
   PRIMARY KEY(league, format)
);

CREATE TABLE PlaysFormat(
   player text NOT NULL,
   class text NOT NULL,
   format text NOT NULL, 
   kills int,
   assists int,
   deaths int,
   kad float,
   healsPerMin float,
   damagePerMin float,
   ubers int,
   drops int,
   FOREIGN KEY(playerID) REFERENCES Player(id),
   FOREIGN KEY(class) REFERENCES Class(name),
   FOREIGN KEY(format) REFERENCES Format(name),
   PRIMARY KEY(playerID, class, format)
);

CREATE TABLE TeamDivision(
   team int NOT NULL,
   division text NOT NULL,
   league text NOT NULL,
   FOREIGN KEY(team) REFERENCES Team(id),
   FOREIGN KEY(league,division) REFERENCES LeagueDivision(league,division),
   PRIMARY KEY(team,division,league)
);
