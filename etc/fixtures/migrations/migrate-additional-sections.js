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

// annotationsSectionREname.keys()

// if (matching)
// {
//   dbentryanntoation[key] = annotationsSectionREname[key]
// }

try {
  const genomicUnits = db.genomic_units.find();

  // read in annotation sections
  // if old section found rename to new section
  print("Starting to loop through each of the engomic units")
  genomicUnits.forEach(element => {
    print("this genomic unit is the above")
    print(element)
    element.annotations.forEach(annotation => {

        const annotation_names = Object.keys(annotation)
        print(annotation_names)
        // const found = annotationOldSections.some(r => keys.includes(r));
        if(found) {
          annotation[annotation_names[0]].forEach(elem => {
            print(elem)
            // if(keys[0] == 'Modelability') {
              
            // }
        });
        }
    })
});

// db.genomic_units.find({'gene': 'VMA21'});


} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
