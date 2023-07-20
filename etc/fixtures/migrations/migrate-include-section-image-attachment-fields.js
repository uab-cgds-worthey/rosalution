const usage = `

mongosh /tmp/fixtures/migrations/migrate-include-section-image-attachment-fields.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval 'var help=true;' /tmp/fixtures/migrations/migrate-include-section-image-attachment-fields.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-include-section-image-attachment-fields.js
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
    let caseUpdated = false;
    element.sections.forEach(section => {
      if ( ['Pedigree', 'Gene To Phenotype', 'Function'].some((value) => {
        return section.header.includes(value);
      }) && !section.hasOwnProperty('attachment_field') ) {        
        section['attachment_field'] = section.header;
        caseUpdated = true;
        print(section);
      }
      
      if ( section.header.includes('Gene to Phenotype') ) {
        const replaced = section.header.replace('to', 'To');
        section.header = replaced;
        section['attachment_field'] = replaced;
        section.content.forEach((row) => {
          if(row.field.includes('Gene to Phenotype')){
            row.field = replaced;
          }
        })
        caseUpdated = true;
        print(section);
      }
    })
    
    if(caseUpdated) {
      print(`  ${element.name} updated...`)
    }

    // update       
    db.analyses.update(
      {'_id': element._id},
      {'$set': element}
    )
    print(`Updated ${element.name} -----`)
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}