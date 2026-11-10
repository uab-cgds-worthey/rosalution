#! /bin/bash
# ./import-analyses-bulk.sh

usage() {
  echo " "
  echo "usage: $0 <options> <json-file-of-analyses>"
  echo " "
  echo " -u Base Rosalution URL"
  echo "    (default) https://local.rosalution.cgds/rosalution"
  echo " -h Prints usage"
  echo " "
  echo "Imports a new Rosalution Analyses for each analysis import data in the JSON file."
  echo " "
  echo "To gather the neccesary Rosalution API credentials, log in to the target"
  echo "Rosalution installation to retrieve the Client ID and Client Secret credentials."
  echo "These are found by clicking on your username or visiting:"
  echo "<rosalution url>/rosalution/account"
  echo " "
  echo " "
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
  exit
}

BASE_URL="https://local.rosalution.cgds/rosalution"

if [ -n "${ROSALUTION_BASE_URL+1}" ]; then
  BASE_URL=$ROSALUTION_BASE_URL
fi

while getopts ":u:h" opt; do
  case $opt in
    u) BASE_URL="$OPTARG";;
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

if ! jq --version &> /dev/null
then
    echo "Error: jq could not be found. Exiting."
    usage
fi

# to get remaining arguments not from getopts
shift "$((OPTIND - 1))"

import_json="$1"

echo "  _____                 _       _   _                   "
echo " |  __ \               | |     | | (_)                  "
echo " | |__) |___  ___  __ _| |_   _| |_ _  ___  _ __        "
echo " |  _  // _ \/ __|/ _\` | | | | | __| |/ _ \| '_ \       "
echo " | | \ \ (_) \__ \ (_| | | |_| | |_| | (_) | | | |      "
echo " |_|  \_\___/|___/\__,_|_|\__,_|\__|_|\___/|_| |_|      "

echo "Rosalution URL: $BASE_URL..."

if [ -z "${ROSALUTION_CLIENT_ID+1}" ]; then
  echo "Please enter your Client Id";
  read -r CLIENT_ID;
else
  CLIENT_ID=$ROSALUTION_CLIENT_ID
fi

if [ -z "${ROSALUTION_CLIENT_SECRET+1}" ]; then
  echo "Please enter your Client Secret";
  read -r -s CLIENT_SECRET;
else
  CLIENT_SECRET=$ROSALUTION_CLIENT_SECRET
fi

if [ -z "${CLIENT_ID}" ] || [ -z "${CLIENT_SECRET}" ]; then
  echo " "
  echo "Please enter required credentials."
  usage
fi

echo "Fetching valid authentication token..."
AUTH_RESPONSE=$(curl -s -k -X 'POST' \
  "$BASE_URL/api/auth/token" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET")
AUTH_TOKEN=$(echo "$AUTH_RESPONSE" |  jq -r '.access_token')

if [[ $AUTH_TOKEN == "null" ]]; then
  echo "Authentication failure; please check credentials"
  exit 1
fi

echo "Opening $import_json"
jq -c '.[]' "$import_json" | while read -r item; do
    analysis_name=$(echo "$item" | jq -r '.external_id')
    echo "Importing Analysis: $analysis_name"
    cpam_project="69e64782bbc494d3fbf6d9b0"
    import_analysis_url="$BASE_URL/api/project/$cpam_project/analysis"
    echo "$item" | curl -s -k -X "POST" \
        "$import_analysis_url" \
        -H "accept: multipart/form-data" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        -F phenotips_file=@- \
        -o /dev/null
        > /dev/null
    echo "Waiting 2 second before importing the next Analysis..."
    sleep 2s
done
