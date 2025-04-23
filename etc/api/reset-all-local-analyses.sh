#! /bin/bash
# ./reset-all-local-analyses.sh

usage() {
  echo " "
  echo "usage: $0"
  echo " "
  echo "Queries the local Rosalution deployment and empties the manifest within"
  echo "each Analysis in the local deployment and then queues new annotations to"
  echo "using the local Rosalution deployment REST API."
  echo " "
  echo "  To reset annotation for all analyses in the local Rosalution deployment the terminal environment must be"
  echo "  sourced using the 'rosalutionrc.sh' script in <rosalution>/etc/api with a user's 'ROSALUTION_CLIENT_ID' and"
  echo "  'ROSALUTION_CLIENT_SECRET' Rosalution API credentials for 'https://local.rosalution.cgds/rosalution'"
  echo " "
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
  exit
}

BASE_URL="https://local.rosalution.cgds/rosalution"
DOCKER_CONTAINER="rosalution-rosalution-db-1"

if [ -n "$1" ]; then
  DOCKER_CONTAINER="$1"
fi

fail=false

if ! jq --version &> /dev/null; then
  echo "❌ Error: jq could not be found. Exiting."
  fail=true
fi

echo "Rosalution URL: $BASE_URL..."
echo ""

if [ -z "${ROSALUTION_CLIENT_ID+1}" ] || [ -z "${ROSALUTION_CLIENT_SECRET+1}" ]; then
  echo "❌ Rosalution API environment credentials 'ROSALUTION_CLIENT_ID' and/or 'ROSALUTION_CLIENT_SECRET' are not set."
  echo "   Source this shell session by sourcing the following script <rosalution-install>/etc/api/rosalutionrc.sh."
  echo ""
  echo "      source rosalutionrc.sh"
  echo ""
  fail=true
fi

if $fail; then
    echo ""
    usage
    exit 1
fi


echo "Fetching valid authentication token..."

AUTH_RESPONSE=$(curl -s -k -X 'POST' \
  "$BASE_URL/api/auth/token" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$ROSALUTION_CLIENT_ID&client_secret=$ROSALUTION_CLIENT_SECRET")
AUTH_TOKEN=$(echo "$AUTH_RESPONSE" |  jq -r '.access_token')

if [[ $AUTH_TOKEN == "null" ]]; then
  echo "Authentication failure; please check credentials"
  exit 1
fi

echo "Fetching existing analyses in Rosalution..."

RESPONSE=$(curl -s -X "GET" \
  "$BASE_URL/api/analysis" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $AUTH_TOKEN")

ANALYSES=()
while IFS='' read -r line; do ANALYSES+=("$line"); done < <(echo "$RESPONSE" | jq -c '[.[].name]')

# Hardcoding to encode the special characters that are commonly
# known in cases being uploaded to Rosalution at this time
echo "${ANALYSES[@]}" | jq -r '.[]' | while read -r ANALYSIS; do
  ./reset-manifest-and-annotate.sh "$DOCKER_CONTAINER" "$ANALYSIS"
  sleep 30s
done

echo "Done. Exiting."