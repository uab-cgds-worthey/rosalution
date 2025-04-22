#! /bin/bash
# ./annotate-analysis.sh

usage() {
  echo " "
  echo "usage: $0 <options> <analysis-name-1> <analysis-name-2> ... <analysis-name-n>"
  echo " "
  echo " -u Base Rosalution URL"
  echo "    (default) https://local.rosalution.cgds/rosalution"
  echo " -h Prints usage"
  echo " "
  echo "Runs annotation for specified analyses. For each analysis after the first, those analyses"
  echo "are queued to annotate after 1 minute."
  echo " "
  echo "To run the annotations, please log in to the target Rosalution installation to retrieve the"
  echo "Client ID and Client Secret credentials. These are found by clicking on your username"
  echo "or visiting: <rosalution url>/rosalution/account"
  echo " "
  echo "Note: This script may need to be run multiple times due to the Rosalution"
  echo "annotation system not being built for large sets of annotations queued."
  echo " "
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
  exit
}

BASE_URL="https://local.rosalution.cgds/rosalution"

if [ -n "${ROSALUTION_BASE_URL+set}" ]; then
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
number_of_analyses=${#@}

echo "  _____                 _       _   _                   "
echo " |  __ \               | |     | | (_)                  "
echo " | |__) |___  ___  __ _| |_   _| |_ _  ___  _ __        "
echo " |  _  // _ \/ __|/ _\` | | | | | __| |/ _ \| '_ \       "
echo " | | \ \ (_) \__ \ (_| | | |_| | |_| | (_) | | | |      "
echo " |_|  \_\___/|___/\__,_|_|\__,_|\__|_|\___/|_| |_|      "
echo "                             _        _   _             "
echo "     /\                     | |      | | (_)            "
echo "    /  \   _ __  _ __   ___ | |_ __ _| |_ _  ___  _ __  "
echo "   / /\ \ | '_ \| '_ \ / _ \| __/ _\` | __| |/ _ \| '_ \ "
echo "  / ____ \| | | | | | | (_) | || (_| | |_| | (_) | | | |"
echo " /_/    \_\_| |_|_| |_|\___/ \__\__,_|\__|_|\___/|_| |_|"

echo "Rosalution URL: $BASE_URL..."

if [ ! -n "${ROSALUTION_CLIENT_ID+set}" ]; then
  echo "Please enter your Client Id";
  read -r CLIENT_ID;
else
  CLIENT_ID=$ROSALUTION_CLIENT_ID
fi

if [ ! -n "${ROSALUTION_CLIENT_SECRET+set}" ]; then
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
AUTH_TOKEN=$(echo $AUTH_RESPONSE |  jq -r '.access_token')
if [[ $AUTH_TOKEN == "null" ]]; then
  echo "Authentication failure; please check credentials"
  exit 1
fi


for ANALYSIS in "$@"; do
  # Hardcoding to encode the special characters that are commonly
  # known in cases being uploaded to Rosalution at this time
  echo "Queueing annotations for analysis '$ANALYSIS'..."
  ANALYSIS=${ANALYSIS/\ /\%20}
  ANALYSIS=${ANALYSIS/\(/\%28}
  ANALYSIS=${ANALYSIS/\)/\%29}
  echo "$BASE_URL/api/annotation/$ANALYSIS"
  curl -s -k -X "POST" \
    "$BASE_URL/api/annotation/$ANALYSIS" \
    -H "accept: application/json" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    > /dev/null
  
  if [  "$number_of_analyses" -gt 1  ]; then
    echo "Waiting 1 minute before queueing next Analysis..."
    sleep 1m
  fi
done
