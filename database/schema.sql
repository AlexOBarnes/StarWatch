DROP TABLE IF EXISTS subscriber_county_assignment, subscriber, forecast, solar_feature, county, body_assignment, body, constellation, region, aurora_alert, aurora_colour, image;

CREATE TABLE image (
    image_id BIGINT GENERATED ALWAYS AS IDENTITY,
    image_name VARCHAR(10) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    image_date DATE NOT NULL,
    PRIMARY KEY (image_id)
);

CREATE TABLE aurora_colour (
    aurora_colour_id SMALLINT,
    colour VARCHAR(6) NOT NULL,
    description VARCHAR(30) NOT NULL,
    meaning VARCHAR(255) NOT NULL,
    PRIMARY KEY (aurora_colour_id)
);

CREATE TABLE aurora_alert (
    alert_id BIGINT GENERATED ALWAYS AS IDENTITY,
    alert_time TIMESTAMP NOT NULL,
    aurora_colour_id SMALLINT NOT NULL,
    PRIMARY KEY (alert_id),
    FOREIGN KEY (aurora_colour_id) REFERENCES aurora_colour(aurora_colour_id)
);

CREATE TABLE region (
    region_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    region_name VARCHAR(25) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    PRIMARY KEY (region_id)
);

CREATE TABLE constellation (
    constellation_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    constellation_name VARCHAR(35) NOT NULL,
    PRIMARY KEY (constellation_id)
);

CREATE TABLE body (
    body_id INT GENERATED ALWAYS AS IDENTITY,
    body_name VARCHAR(35) NOT NULL,
    constellation_id SMALLINT,
    PRIMARY KEY (body_id),
    FOREIGN KEY (constellation_id) REFERENCES constellation(constellation_id)
);

CREATE TABLE body_assignment (
    assignment_id BIGINT GENERATED ALWAYS AS IDENTITY,
    region_id SMALLINT NOT NULL,
    body_id BIGINT NOT NULL,
    begin_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id),
    FOREIGN KEY (body_id) REFERENCES body(body_id)
);

CREATE TABLE county (
    county_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    county_name VARCHAR(35) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    region_id SMALLINT NOT NULL,
    PRIMARY KEY (county_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);

CREATE TABLE solar_feature (
    sunrise_id BIGINT GENERATED ALWAYS AS IDENTITY,
    sunrise_timestamp TIMESTAMP NOT NULL,
    sunset_timestamp TIMESTAMP NOT NULL,
    county_id SMALLINT NOT NULL,
    PRIMARY KEY (sunrise_id),
    FOREIGN KEY (county_id) REFERENCES county(county_id)
);

CREATE TABLE forecast (
    forecast_id BIGINT GENERATED ALWAYS AS IDENTITY,
    county_id SMALLINT NOT NULL,
    temperature_c FLOAT NOT NULL,
    precipitation_probability_percent SMALLINT NOT NULL,
    precipitation_mm FLOAT NOT NULL,
    cloud_coverage_percent SMALLINT NOT NULL,
    visibility_m SMALLINT NOT NULL,
    at TIMESTAMP NOT NULL,
    PRIMARY KEY (forecast_id),
    FOREIGN KEY (county_id) REFERENCES county(county_id)
);

CREATE TABLE subscriber (
    subscriber_id BIGINT GENERATED ALWAYS AS IDENTITY,
    subscriber_username VARCHAR(30) NOT NULL,
    subscriber_phone VARCHAR(15),
    subscriber_email VARCHAR(255),
    PRIMARY KEY (subscriber_id),
    CONSTRAINT phone_or_email_exist CHECK (
        subscriber_phone IS NOT NULL OR subscriber_email IS NOT NULL
    )
);

CREATE TABLE subscriber_county_assignment (
    assignment_id BIGINT GENERATED ALWAYS AS IDENTITY,
    subscriber_id BIGINT NOT NULL,
    county_id SMALLINT NOT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (subscriber_id) REFERENCES subscriber(subscriber_id),
    FOREIGN KEY (county_id) REFERENCES county(county_id)
);
