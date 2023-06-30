const usage = `
mongosh /tmp/fixtures/migrations/migrate-new sections-phenotips-importer.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/migrations/migrate-new-sections-phenotips-importer.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-new-sections-phenotips-importer.js
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

// use new sections in phenotips importer in import_analysis_data to reconfigure database and move the data
// can we just use the config in phenotips importer? without creating an array/object here?
// const newSectionsRename = [
//   {
//       "header": str(phenotips_json_data["gene"] + "Gene to Phenotype (like pedigree)"), "content":[]
//   }, {
//       "header": str(phenotips_json_data["gene"] + "Molecular Mechanism"), "content":[
//           {"field": 'Function', "value": []}
//       ]
//   },{
//       "header": str(phenotips_json_data["gene"] + "Function"), "content":[]
//   },{
//       "header": 'Model Goals', "content": [
//           {"field": 'Model of Interest', "value": []},
//           {"field": 'Goals', "value": []},
//           {"field": 'Proposed Model/Project', "value": []},
//           {"field": 'Existing Collaborations', "value": []},
//           {"field": 'Existing Funding', "value": []},
//     ]
//   }
// ]

try {
  const analyses = db.analyses.find();
  analyses.forEach(element => {
    element.sections.forEach(section => {
        const value = Object.values(section)
        
        print(value)
        // add new sections to sections[] in each element
        // check if field already exists in analyses sections 
        //move field data
        // update

          
          // db.genomic_units.update(
          //   {'_id': element._id},
          //   {'$set': element}
          // )
    })
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}