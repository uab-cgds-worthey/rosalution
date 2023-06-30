#! /bin/bash
# ./annotate-all-existing-analyses.sh

usage() {
  echo " "
  echo "usage: $0"
  echo " "
  echo " -h Prints usage"
  echo " "
  echo "Kicks off annotation jobs for all the existing analyses in Rosalution"
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

while getopts ":h" opt; do
  case $opt in
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

if ! jq --version &> /dev/null
then
    echo "Error: jq could not be found. Exiting."
    usage
fi

echo "Please enter your Client Id";
read -r CLIENT_ID;

echo "Please enter your Client Secret";
read -r -s CLIENT_SECRET;

if [ -z "${CLIENT_ID}" ] || [ -z "${CLIENT_SECRET}" ]; then
  echo " "
  echo "Please enter required credentials."
  usage
fi

echo "Fetching valid authentication token..."

AUTH_TOKEN=$(curl -s -X 'POST' \
  "http://local.rosalution.cgds/rosalution/api/auth/token" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=&scope=&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET" | jq -r '.access_token')

echo "Fetching existing analyses in Rosalution..."

RESPONSE=$(curl -s -X "GET" \
  "http://local.rosalution.cgds/rosalution/api/analysis/" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $AUTH_TOKEN")

ANALYSES=()
while IFS='' read -r line; do ANALYSES+=("$line"); done < <(echo "$RESPONSE" | jq -c '[.[].name]')

echo "${ANALYSES[@]}" | jq -r '.[]' | while read -r ANALYSIS; do
  echo "Starting annotations for analysis $ANALYSIS..."
  curl -s -X "POST" \
      "http://local.rosalution.cgds/rosalution/api/annotate/$ANALYSIS" \
      -H "accept: application/json" \
      -H "Authorization: Bearer $AUTH_TOKEN" \
      > /dev/null
  sleep 5
done

echo "Done. Exiting."