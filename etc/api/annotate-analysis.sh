#! /bin/bash
# ./annotate-all-existing-analyses.sh

usage() {
  echo " "
  echo "usage: $0"
  echo " "
  echo " -u Base Rosalution URL"
  echo "    (default) http://local.rosalution.cgds/rosalution"
  echo " -h Prints usage"
  echo " "
  echo "Runs annotation for a specified analysis. "
  echo " "
  echo "To run the annotations, please log in to Rosalution to retrieve the"
  echo "Client ID and Client Secret credentials. These can be found by"
  echo "clicking on your username or going to: <rosalution url>/rosalution/account"
  echo " "
  echo "Note: This script may need to be run multiple times due to the Rosalution"
  echo "annotation system not being built for large sets of annotations queued."
  echo " "
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
  exit
}

BASE_URL="http://local.rosalution.cgds/rosalution"

if [[ -v ROSALUTION_BASE_URL ]]; then
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
echo "  $@"
echo ""


if [[ ! -v ROSALUTION_CLIENT_ID ]]; then
  echo "Please enter your Client Id";
  read -r CLIENT_ID;
else
  CLIENT_ID=$ROSALUTION_CLIENT_ID
fi

if [[ ! -v ROSALUTION_CLIENT_SECRET ]]; then
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

AUTH_TOKEN=$(curl -s -X 'POST' \
  "$BASE_URL/api/auth/token" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET" | jq -r '.access_token')

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
  curl -s -X "POST" \
    "$BASE_URL/api/annotation/$ANALYSIS" \
    -H "accept: application/json" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    > /dev/null
done
