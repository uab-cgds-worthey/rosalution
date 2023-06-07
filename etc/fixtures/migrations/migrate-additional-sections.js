const usage = `
mongosh /tmp/fixtures/migrations/migrate-additional-sections.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/migrations/migrate-additional-sections.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-additional-sections.js
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

const annotationSectionsRename = {
  'Modelability': 'Orthology',
  'Protein Expression': 'Human Gene Expression',
}

try {
  const genomicUnits = db.genomic_units.find();
  genomicUnits.forEach(element => {
    element.annotations.forEach(annotation => {
        const annotation_name = Object.keys(annotation)
        
        if (annotationSectionsRename[annotation_name]) {
          Object.assign(annotation, {[annotationSectionsRename[annotation_name]]: annotation[annotation_name]})
          delete annotation[annotation_name]
          
          db.genomic_units.update(
            {'_id': element._id},
            {'$set': element}
          )
        }
    })
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
