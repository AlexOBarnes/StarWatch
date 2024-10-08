source .env
export PGPASSWORD=$DB_PASSWORD
if [ -z "$1" ]; then
  echo "Please provide a valid SQL query as an argument."
  exit 1
fi
psql -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME -c "$1"