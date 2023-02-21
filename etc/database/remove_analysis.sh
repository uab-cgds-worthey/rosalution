#! /bin/sh
# ./initial-db-seed.sh -h <host> -f <datasource>
usage() {
  echo "usage: $0 -h <host>"
  echo " "
  echo " -h MongoDB host URL"
  echo "    (default) localhost:27017"
  echo " "
  echo "Seeds the initial Rosalution database with base fixtures for local development and system testing"
  exit
}

analysisName=""
docker_prefix=""
connection_string="localhost:27017"

while getopts ":a:d:h" opt; do
  case $opt in
    a) mongodb_host=$OPTARG;;
    d) docker_prefix="docker exec -t ${OPTARG}";;
    c) connection_string=$OPTARG;;
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

database="rosalution_db"

in='$in'

echo "Which Analysis would you like to remove:"
read analysisName

echo "Finding Analysis..."
analysis=$(${docker_prefix} mongosh --quiet --eval "'db.analyses.find({'name': {$in: ['$analysisName']}}, {_id: true});'" $database | cut -d'"' -f 2)

echo $analysis

if [ -z "$analysis" ]; then
   echo "${analysisName} not found.";
   exit;
fi

echo "Found ${analysis} of ${analysisName}. Would you like to remove them [Y/n]:"
# read response

# echo "Removing "
