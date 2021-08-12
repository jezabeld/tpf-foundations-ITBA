CREATE TABLE IF NOT EXISTS locations(
    iso_code varchar(3) UNIQUE,
    location varchar(50) UNIQUE,
    continent varchar(20),
    population bigint,
    PRIMARY KEY(iso_code, location)
);

CREATE TABLE IF NOT EXISTS daily_stats(
    date date ,
    iso_code varchar(3),
    total_cases bigint,
    new_cases int,
    total_deaths bigint,
    new_deaths int,
    total_tests bigint,
    new_tests int,
    new_vaccinations int,
    total_vaccinations bigint,
    people_vaccinated bigint,
    PRIMARY KEY(date, iso_code),
    CONSTRAINT fk_iso_code
      FOREIGN KEY(iso_code) 
	  REFERENCES locations(iso_code)
);

CREATE TABLE IF NOT EXISTS vaccines(
    date date,
    location varchar(50),
    manufacturer varchar(50),
    total_vaccinations int,
    PRIMARY KEY(date, location, manufacturer),
    CONSTRAINT fk_location
      FOREIGN KEY(location) 
	  REFERENCES locations(location)
);