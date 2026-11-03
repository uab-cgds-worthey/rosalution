const usage = `

mongosh /tmp/fixtures/migrations/migrate-supporting-evidence-to-attachments.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval 'var help=true;' /tmp/fixtures/migrations/migrate-supporting-evidence-to-attachments.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-supporting-evidence-to-attachments.js
`

if (help === true) {
    print(usage);
    quit(1);
}

if (typeof databaseName === 'undefined') {
    databaseName = 'rosalution_db';
} else if (typeof databaseName !== 'string') {
    print('databaseName must be a string');
    quit(1);
}

db = db.getSiblingDB(databaseName);

try {
  const analyses = db.analyses.find();
  analyses.forEach(element => {
    print(`Migrating case ${element.name} -----`)
    
    let analysisUpdated = false;
    element['attachments'] = element.supporting_evidence_files
    element.sections.forEach(section => {
      section.content.forEach(field => {
        if(field.type == "section-supporting-evidence") {
          field.type = "section-attachment"
          analysisUpdated = true
        }
      });
    })
    
    if(analysisUpdated) {
      print(`  ${element.name} updated...Section Attachments`)
    }

    db.analyses.update(
      {'_id': element._id},
      {'$set': element}
    )
    print(`  ${element.name} updated...Attachments`)
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}