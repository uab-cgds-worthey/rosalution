#! /bin/bash
# ./remove-analysis.sh -c <mongo_connection_string> -d <docker_container_name> -m <mongo_database>
usage() {
  echo " "
  echo "usage: $0 -c <mongo_connection_string> -d <docker_container_name> -m <mongo_database>"
  echo " "
  echo " -c MongoDB connection string"
  echo "    (default) localhost:27017"
  echo " -d Docker container running Mongo"
  echo "    Find with 'docker ps' command"
  echo " -m Mongo database name"
  echo "    (default) rosalution_db"
  echo " -h Usage"
  echo " "
  echo "Removes Rosalution Analyses from Mongo."
  exit
}

docker_prefix=""
connection_string="localhost:27017"
database="rosalution_db"

while getopts ":c:d:m:h" opt; do
  case $opt in
    c) connection_string=$OPTARG;;
    d) docker_prefix="docker exec ${OPTARG}";;
    m) database=$OPTARG;;
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

mongo_host=$(echo "$connection_string" | cut -d: -f1)
mongo_port=$(echo "$connection_string" | cut -d: -f2)

echo "Which Analysis would you like to remove:"
read -r analysisName

echo "Finding Analysis..."
analysis=$(${docker_prefix} mongosh --host "$mongo_host" --port "$mongo_port" --quiet --eval "'db.analyses.find({'name': '$analysisName'}, {_id: true}).count();'" "$database")

if [ "$analysis" = "0" ]; then
   echo "${analysisName} not found.";
   exit;
fi

read -p "Found ${analysis} of ${analysisName}. Would you like to remove it [y/N]: " -n 1 -r
echo

if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
  echo "Cancelling."
  exit;
fi

echo "Removing..."
${docker_prefix} mongosh --host "$mongo_host" --port "$mongo_port" --quiet --eval "'db.analyses.deleteOne({'name': '$analysisName'});'" "$database"

echo "Done."
