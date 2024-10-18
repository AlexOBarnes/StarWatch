# ✨ StarWatch ✨

## 📝 Background
#### 🛠️ **Problem statement**:
There are too many different sources of information about the night sky for amateur astronomers.

For example, imagine you are an amateur astronomer who is thinking about stargazing tonight. You might use a Night Sky app to find out what celestial bodies (planets/stars/etc) are in the sky at night, but then you also check the weather forecast to make sure it isn’t cloudy or raining tonight. Then, you have to find a way to check when the sun sets and rises or what phase the moon is in (so you know when it’s dark enough to stargaze). Then wouldn’t it also be cool to find out if there is Aurora activity or a meteor shower tonight?

All of this info may be available to the general public, but it is incredibly inconvenient to have to download many mobile apps, or navigate through various websites, just to get prepared for an astronomical venture.

## 🎯 Project Goals
A dashboard or website which may include:
- Night Sky forecast (e.g. star charts and weather)
- Aurora activity
- Upcoming events (e.g. meteor shower or solar eclipse)
- Analysis of past events (e.g. how frequently has X planet been visible from Y region in the past month)
Email or phone alerts for subscribers:
- For sudden spikes in aurora activity
- Ahead of time alerts - e.g. “Jupiter will be very visible in your location in an hour”

## 📂 Directories

### 🧰 `/assets`
Contains all simplified visual overviews of different aspects of the project architecture, namely:

1. [AWS RDS Entity Relationship Diagram](/assets/ERD_starwatch.png)
2. [Infrastructure Architecture Diagram](/assets/starwatch_architecture_diagram.png)
3. [Streamlit Dashboard Wireframe](/assets/starwatch_dashboard_wireframe.png)

### 🔭 `/astronomy-pipeline`
Contains the files necessary to run the weekly astronomy ETL pipeline that uses data from the [Astronomy API](https://astronomyapi.com/).

This data source was used to obtain information up to two weeks in advance regarding:  
1. The relative location of celestial bodies within our solar system from different counties around the UK.
2. Daily data on the moon phase as visible from the UK
3. Star charts of different stellar constellations as visible from the UK.

For instructions on running this pipeline please see the [Astronomy README](/astronomy-pipeline/README.md).

### 🌌 `/aurorawatch-pipeline`
Contains the files necessary to run the hourly ETL pipeline that uses data from the [AuroraWatch API](https://aurorawatch.lancs.ac.uk/).

This data source was used to obtain information regarding the current aurora activity in the UK.

For instructions on running this pipeline please see the [AuroraWatch README](/aurorawatch-pipeline/README.md).

### 🧑‍💻 `/dashboard`
Contains the files necessary to run the StarWatch dashboard service which is run using an AWS ECS Service. This analyses the data from all of this project's data pipelines to create insightful visualisations.

This dashboard also provides users with the ability to subscribe to StarWatch for personalised astronomy SMS alerts.

For instructions on running the dashboard please see the [Dashboard README](/dashboard/README.md).

The [Dashboard Wireframe](/assets/starwatch_dashboard_wireframe.png) provides an overview of the visualisations that are displayed by this service.

### 💾 `/database`
Contains files that simplify the process of experimenting with and testing the RDS database linked to this repository.

The [Database ERD](/assets/ERD_starwatch.png) shows the structure of this database.

These files consist of:

`.sh` files that can be run from the terminal using:
```bash
bash [filename.sh]
```

`.sql` files that can be run from the terminal using:
```bash
psql -U [database_username] -d [database_name] -f [path_to_file.sql]
```

For more information on these files and how to use them, please see the [Database README](/database/README.md).

### 🌦️ `/quadhoral-openmeteo`
Contains the files necessary to run the quadhoral OpenMeteo ETL pipeline that uses data from the [OpenMeteo API](https://open-meteo.com/).

This pipeline extracted a range of UK weather related information that was updated every four hours to ensure that the data remained accurate and reliable.

For instructions on running this pipeline please see the [Quadhoral OpenMeteo README](/quadhoral-openmeteo/README.md).

### 🌅 `/weekly-openmeteo`
Contains the files necessary to run the weekly OpenMeteo ETL pipeline that extracts sunrise and sunset data from the [OpenMeteo API](https://open-meteo.com/).

For instructions on running this pipeline please see the [Weekly OpenMeteo README](/weekly-openmeteo/README.md).

### 📲 `/sms-checker`
Contains the files necessary to run an hourly ETL pipeline that analyses database data and sends alerts to subscribed users in the event that there is an upcoming or ongoing astronomical event in their area.

For more information on this service please see the [SMS Checker README](/sms-checker/README.md).

### 🏗️ `/terraform`
Contains the files necessary for automating the building and deconstruction of the AWS resources necessary for this project's [cloud architecture](/assets/starwatch_architecture_diagram.png).

For more detailed information on how to use these resources, please see the [Terraform README](/terraform/README.md).

#### ⛔️ `.gitignore`
Contains the file names/types that should only be stored locally and not uploaded to github or shared otherwise.

These files largely fall into two categories:

1. Sensitive information (eg. '_**env**_' files)
2. Local data stores (eg. '_**.csv**_' files, '_**.json**_' files)

If new file format is added locally, or new sensitive information is added to the repository, these should be included as new lines in the `.gitignore` file.
