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

db = db.getSiblingDB(databaseName);

try {
  const analyses = db.analyses.find();
  analyses.forEach(element => {
    // print(element)

    // from each analysis get each gene for the gene specific sections
    // maybe store it in an array? 
    genes = []
    element.genomic_units.forEach(unit => {
      if (unit.gene) {
        genes.push(unit.gene)
      }
    })
    print(genes)

    //iterating through the genes array to append the gene sections here
    genes.forEach(gene => {
      print ("APPENDING GENE SECTIONS HERE TO element.sections")
    })

    element.sections.forEach(section => {
      const value = Object.values(section)
      
      // print(value)

      
      // add new sections to sections[] in each element
      // check if field already exists in analyses sections 
      //move field data -- how????

    })

    // update       
    // db.analyses.update(
    //   {'_id': element._id},
    //   {'$set': element}
    // )
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}