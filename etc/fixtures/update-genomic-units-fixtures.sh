#! /bin/bash
# ./update-genomic-units-fixtures.sh -d <docker-container> -c <mongo_connection_string> -m <mongo_database>

usage() {
    echo " "
    echo "usage: $0"
    echo " "
    echo " -d docker container name"
    echo "    Find with 'docker ps' command"
    echo " -c MongoDB connection string"
    echo "    (default) localhost:27017"
    echo " -m Mongo database name"
    echo "    (default) rosalution_db"
    echo " "
    echo " -h Prints usage"
    echo " "
    echo "Automatically updates the genomic_units.json fixtures for the initial mongo seed"
    echo "when deploying a fresh version of Rosalution."
    echo " "
    echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
    echo " "
    echo "Example usage:"
    echo " ./update-genomic-units-fixtures.sh"
    echo " ./update-genomic-units-fixtures.sh -d rosalution-rosalution-db-1 -c localhost:27017 -m rosalution_db"
    echo " "
    exit
}

# Parent file of this script. 
# This is found so the Rosalution genomic_units.js fixture
# can be updated regardless of where this script is run.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd -P)

MONGODB_CONNECTION_STRING="localhost:27017"
MONGODB_DATABASE_NAME="rosalution_db"
MONGODB_COLLECTION="genomic_units"

DOCKER_CONTAINER_NAME=""
DOCKER_EXEC_PREFIX=""

while getopts "d:c:m:h" opt; do
  case $opt in
    d) DOCKER_CONTAINER_NAME=$OPTARG && DOCKER_EXEC_PREFIX="docker exec $DOCKER_CONTAINER_NAME";;
    c) MONGODB_CONNECTION_STRING=$OPTARG;;
    m) MONGODB_DATABASE_NAME=$OPTARG;;
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

MONGO_CONNECTION_HOST=$(echo "$MONGODB_CONNECTION_STRING" | cut -d: -f1)
MONGO_CONNECTION_PORT=$(echo "$MONGODB_CONNECTION_STRING" | cut -d: -f2)

${DOCKER_EXEC_PREFIX} mongoexport --host "$MONGO_CONNECTION_HOST" --port "$MONGO_CONNECTION_PORT" --jsonArray --collection="$MONGODB_COLLECTION" --db="$MONGODB_DATABASE_NAME" --out=/tmp/genomic-units.json --pretty

if [ -n "$DOCKER_CONTAINER_NAME" ]
then
    docker cp "$DOCKER_CONTAINER_NAME":/tmp/genomic-units.json /tmp/
    ${DOCKER_EXEC_PREFIX} rm -rf /tmp/genomic-units.json
fi

jq 'del(.[]._id)' /tmp/genomic-units.json > /tmp/genomic-units.tmp && mv /tmp/genomic-units.tmp "$PARENT_PATH"/initial-seed/genomic-units.json

rm /tmp/genomic-units.json

echo "Done. Exiting."
