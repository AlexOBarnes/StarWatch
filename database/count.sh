source .env
export PGPASSWORD=$DB_PASSWORD

row_count=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -A -c 'SELECT COUNT(*) FROM solar_feature;' | xargs)
echo "Number of rows in solar_feature table: $row_count"

forecast_count=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -A -c 'SELECT COUNT(*) FROM forecast;' | xargs)
echo "Number of rows in forecast table: $forecast_count"

body_count=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -A -c 'SELECT COUNT(*) FROM body_assignment;' | xargs)
echo "Number of rows in body_assignment table: $body_count"

aurora_count=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -A -c 'SELECT COUNT(*) FROM aurora_alert;' | xargs)
echo "Number of rows in aurora_alert table: $aurora_count"

image_count=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -A -c 'SELECT COUNT(*) FROM image;' | xargs)
echo "Number of rows in image table: $image_count"