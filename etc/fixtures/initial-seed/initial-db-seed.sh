#! /bin/bash
# ./initial-db-seed.sh -h <host> -f <datasource>
usage() {
  echo "usage: $0 -h <host> -f <datasource>"
  echo " "
  echo " -h MongoDB host URL"
  echo "    (default) localhost:27017"
  echo " -f Fixtures filepath"
  echo "    (default) /tmp/fixtures/initial-seed"
  echo " "
  echo "Seeds the initial Rosalution database with base fixtures for local development and system testing"
  exit
}

while getopts ":a:v:h" opt; do
  case $opt in
    a) mongodb_host=$OPTARG;;
    v) fixture_filepath=${OPTARG};;
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

if [[ ! -v mongodb_host ]] ; then
  mongodb_host="localhost:27017"
fi

if [[ ! -v fixture_filepath ]] ; then
  fixture_filepath="/tmp/fixtures/initial-seed"
fi

echo "Seeding Rosalution database..."

database="rosalution_db"

echo "Importing Analyses..."

mongoimport  --db "$database" --collection analyses --file "$fixture_filepath/analyses.json" --jsonArray

echo "Importing Dataset Sources..."
mongoimport  --db "$database" --collection dataset_sources --file "$fixture_filepath/dataset-sources.json" --jsonArray

echo "Importing Users..."
mongoimport  --db "$database" --collection users --file "$fixture_filepath/users.json" --jsonArray

echo "Seeding Rosalution databse...Complete"
