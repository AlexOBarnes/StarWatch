# StarWatch Database
This folder contains the scripts to create the database, database tables(as shown in _Figure 1_) and seed each table with static data. There are shell scripts included that automate distinct tasks related to resetting, seeding and querying the database

## Design
![ERD](../assets/ERD_starwatch.png)
__Figure 1__ - _Starwatch Database ERD_: Shows the entity relationship diagram for the database used in this project.

## Setup
1. Ensure that an SQL server RDS has been setup prior and is accessible.
    - Note: be sure to store the credentials for accessing this database safely.

2. Create a `.env` file with the following:
    - DB_HOST - to access your RDS instance
    - DB_USER - username for accessing RDS
    - DB_PASSWORD - password for accessing RDS
    - DB_NAME - the name of your database
    - DB_PORT - port to access RDS (typically 5432 for postgres)

## Usage

## How it works