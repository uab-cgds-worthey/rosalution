#! /bin/bash
# ./backup-analyses-manifest-to-files.sh <docker-container> <output-path (optional)>"

usage() {
  echo "usage: $0 <docker-container> <output-path (optional)>"
  echo " "
  echo "Creates a JSON file for each Rosalution Analysis from the Rosalution MongoDB database named"
  echo " 'rosalution-analysis-manifset-<analysis name>-<current-date>.json'"
  echo "to the designated output path. By default, the output path is '${pwd}/manifests-backup/'"
  echo "Include a second paramater to overwrite the <output-path>.  If the <output-path> does not exist, the script"
  echo "will try to create it."
}

if [[ $# -eq 0 ]]
then
    echo "Missing required input. Exiting script ..."
    echo ""

    usage
    exit 1
fi

DOCKER_CONTAINER=$1
TARGET_PATH="$(pwd)/manifests-backup"

if [[ $# -eq 2 ]]
then
    TARGET_PATH=$2
fi

mkdir -p "$TARGET_PATH"

if [[ ! -d "$TARGET_PATH" ]]
then
    echo "Target output file path '$TARGET_PATH' does not exist.  Canceling backup operation ..."
    echo ""

    usage
    exit 1
fi

date_stamp=$(date +"%Y-%m-%ds")
result=$(docker exec rosalution-rosalution-db-1 mongosh rosalution_db --quiet --eval 'JSON.stringify(db.analyses.find({}, {_id: 0, name:1}).toArray());' )
echo $result
ANALYSES=()
while IFS='' read -r line; do ANALYSES+=("$line"); done < <(echo "$result" | jq -c '[.[].name]')

echo "Creating analysis manifest backup..."
echo "------------------------------------"
echo "${ANALYSES[@]}" | jq -r '.[]' | while read -r ANALYSIS; do
  echo "$ANALYSIS"
  eval_string="JSON.stringify(db.analyses.findOne({\"name\": \"$ANALYSIS\"}, {_id: 0, manifest:1}));"
  manifest_result=$(docker exec rosalution-rosalution-db-1 mongosh rosalution_db --quiet --eval "'${eval_string}'")
  echo $manifest_result | jq . > "$TARGET_PATH/rosalution-analysis-manifset-$ANALYSIS-$date_stamp.json"
done
