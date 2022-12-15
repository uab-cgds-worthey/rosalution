#! /bin/bash
# ./restore-database.sh <docker-container> <target-restore-database-archive>
usage() {
  echo "usage: $0 <docker-container> <target-database-restore-archive>"
  echo "  Restores an archived 'rosalution_db', a rosalution mongodb database, into the specified"
  echo "  MongoDB docker container. The filepath for <target-restore-database-archive> must be an"
  echo "  absolute file path on the system."
}

if [[ $# -ne 2 ]]
then
    echo "Missing required input. Exiting script ..."
    echo ""

    usage
    exit 1
fi

DOCKER_CONTAINER=$1
MONGODB_ARCHIVE_FILEPATH=$2
MONGODB_ARCHIVE=$(basename "$MONGODB_ARCHIVE_FILEPATH")

docker cp "$MONGODB_ARCHIVE_FILEPATH" "$DOCKER_CONTAINER":/home/"$MONGODB_ARCHIVE"
docker exec "$DOCKER_CONTAINER" sh -c "exec mongorestore --nsInclude 'rosalution_db.*' --drop --archive=/home/$MONGODB_ARCHIVE"