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
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
  exit
}

if ! jq --version &> /dev/null
then
    echo "Error: jq could not be found. Exiting."
    usage
fi

# Environment variables
CLIENT_ID="3bghhsmnyqi6uxovazy07ryn9q1tqbnt"
CLIENT_SECRET="i1y0ESKVt3ZWLrxL7wiVkokS1gYrchXX"

while getopts ":h" opt; do
  case $opt in
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

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

ANALYSES=(`echo $RESPONSE | jq -c '[.[].name]'`)

echo $ANALYSES | jq -r '.[]' | while read ANALYSIS; do
  echo "Starting annotations for analysis $ANALYSIS..."
  curl -s -X "POST" \
      "http://local.rosalution.cgds/rosalution/api/annotate/$ANALYSIS" \
      -H "accept: application/json" \
      -H "Authorization: Bearer $AUTH_TOKEN" \
      > /dev/null
  sleep 5
done

echo "Done. Exiting."