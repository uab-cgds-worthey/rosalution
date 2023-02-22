#! /bin/sh
# ./remove_analysis.sh -c <mongo_connection_string> -d <docker_container_name> -m <mongo_database>
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

echo "Which Analysis would you like to remove:"
read analysisName

echo "Finding Analysis..."
analysis=$(${docker_prefix} mongosh --quiet --eval "'db.analyses.find({'name': /$analysisName/}).count();'" $database)

if [ "$analysis" = "0" ]; then
   echo "${analysisName} not found.";
   exit;
fi

read -p "Found ${analysis} of ${analysisName}. Would you like to remove them [y/N]: " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  echo "Cancelling."
  exit;
fi

echo "Removing..."
${docker_prefix} mongosh --quiet --eval "'db.analyses.deleteMany({'name': /$analysisName/});'" $database

echo "Done."