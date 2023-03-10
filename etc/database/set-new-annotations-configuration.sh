#! /bin/bash
# ./remove-analysis.sh -f <annotation-config-collection-json-file-path> -c <mongo_connection_string> -d <docker_container_name> -m <mongo_database> -b backup-directory

usage() {
  echo " "
  echo "usage: $0 -f <annotation-config-collection-json-file-path> -c <mongo_connection_string> -d <docker_container_name> -m <mongo_database> -b backup-directory"
  echo " "
  echo " -f Annotation Configuration JSON file path"
  echo "    (required)"
  echo " -c MongoDB connection string"
  echo "    (default) localhost:27017"
  echo " -d Docker container running Mongo"
  echo "    Find with 'docker ps' command"
  echo " -m Mongo database name"
  echo "    (default) rosalution_db"
  echo " -b backup directory path to save the existing annotation configuration collection json"
  echo "    (default) /home/centos/backups/rosalution-annotation-configuration-backup  "
  echo " "
  echo " -h Prints usage"
  echo " "
  echo "Backups the existing Rosalution Annotation Configuration as an Extended JSON with the current date to the backup directory."
  echo "Then replaces the existing collection with the provided annotation configuration."
  echo " "
}

target_backup_path=/home/centos/backups/rosalution-annotation-configuration-backup
docker_container_name=""
connection_string="localhost:27017"
database="rosalution_db"
annotation_configuration_filepath=""

while getopts "f:b:c:d:m:h" opt; do
  case $opt in
    f) annotation_configuration_filepath=$OPTARG;;
    c) connection_string=$OPTARG;;
    d) docker_container_name=$OPTARG;;
    m) database=$OPTARG;;
    b) target_backup_path=$OPTARG;;
    h) usage && exit;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

docker_exec_prefix="docker exec $docker_container_name"

if [ "$annotation_configuration_filepath" = "" ]
then
  echo "Missing required paramater: -f annotation_configuration_filepath. Canceling update operation ..."
  echo ""

  usage
  exit 2
fi

mongo_host=$(echo "$connection_string" | cut -d: -f1)
mongo_port=$(echo "$connection_string" | cut -d: -f2)

if [[ ! -d "$target_backup_path" ]]
then
    echo "Target output file path '$target_backup_path' does not exist.  Canceling update operation ..."
    echo ""

    usage
    exit 2
fi

date_stamp=$(date +"%Y-%m-%d-%s")
target_backup_filepath="$target_backup_path/annotation-config-$date_stamp.json"
${docker_exec_prefix} mongoexport --host "$mongo_host" --port "$mongo_port" --db "$database" --collection="annotations_config" --out="$target_backup_filepath"

target_configuration_filepath="$annotation_configuration_filepath"
if [ "$docker_container_name" != "" ]
then
  docker cp "$docker_container_name":"$target_backup_filepath" "$target_backup_filepath"
  target_configuration_filename=$(basename "$annotation_configuration_filepath")

  #Updates the target annotation configuration filepath to be the filepath within the docker container instead of the local machine
  target_configuration_filepath="/home/$target_configuration_filename"
  docker cp "$annotation_configuration_filepath" "$docker_container_name":"$target_configuration_filepath"
fi

${docker_exec_prefix} mongoimport --host "$mongo_host" --port "$mongo_port" --db "$database" --collection="annotations_config" --drop --file "$target_configuration_filepath" --jsonArray