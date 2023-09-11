const usage = `
mongosh /tmp/fixtures/migrations/migrate-add-decisions.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/migrations/migrate-add-decisions.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-add-decisions.js
`

if (help === true) {
    print(usage);
    quit(1);
}

if (typeof databaseName === 'undefined') {
    databaseName = "rosalution_db";
} else if (typeof databaseName !== 'string') {
    print("databaseName must be a string");
    quit(1);
}

db = db.getSiblingDB(databaseName);

const acmgRowsToBrief = [
  'ACMG Classification',
  'ACMG Classification Criteria',
  'ACMG Criteria To Add'
]

try {
  const analyses = db.analyses.find();
  analyses.forEach(element => {
    print(`Migrating case ${element.name} -----`)

    // Add Decision Section to Brief 
    const briefSection = element.sections.find( section => section.header === 'Brief');

    acmgRowsToBrief.forEach(newRow => {
      if( !briefSection.content.find(row => row.field === newRow) ) {
        briefSection.content.push({
          'type': 'section-text',
          'field': newRow,
          value: [],
        });
      };
    });

    db.analyses.updateOne(
      {'_id': element._id},
      {'$set': element}
    );
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
