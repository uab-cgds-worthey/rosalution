docker exec -it rosalution-rosalution-db-1 mongoexport --jsonArray --collection=genomic_units --db=rosalution_db --out=genomic-units.json --pretty

docker cp rosalution-rosalution-db-1:genomic-units.json /tmp/

jq 'del(.[]._id)' /tmp/genomic-units.json > /tmp/genomic-units.tmp && mv /tmp/genomic-units.tmp ./initial-seed/genomic-units.json

rm /tmp/genomic-units.json
