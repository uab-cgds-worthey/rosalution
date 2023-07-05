const usage = `
mongosh /tmp/fixtures/migrations/migrate-new sections-phenotips-importer.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval 'var help=true;' /tmp/fixtures/migrations/migrate-new-sections-phenotips-importer.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-new-sections-phenotips-importer.js
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

// use new sections in phenotips importer in import_analysis_data to reconfigure database and move the data
// can we just use the config in phenotips importer? without creating an array/object here?
// const newSectionsRename = [
//   {
//       'header': str(phenotips_json_data['gene'] + 'Gene to Phenotype (like pedigree)'), 'content':[]
//   }, {
//       'header': str(phenotips_json_data['gene'] + 'Molecular Mechanism'), 'content':[
//           {'field': 'Function', 'value': []}
//       ]
//   },{
//       'header': str(phenotips_json_data['gene'] + 'Function'), 'content':[]
//   },{
//       'header': 'Model Goals', 'content': [
//           {'field': 'Model of Interest', 'value': []},
//           {'field': 'Goals', 'value': []},
//           {'field': 'Proposed Model/Project', 'value': []},
//           {'field': 'Existing Collaborations', 'value': []},
//           {'field': 'Existing Funding', 'value': []},
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

    //iterating through the genes array to create the gene sections here
    if (genes.length > 0) {
      genes.forEach(gene => {
        print (`${gene} APPENDING GENE SECTIONS HERE TO element.sections`)
        newGeneSections = [{
            "header": gene.concat(" Gene to Phenotype"), "content": [
                {"type": "images-dataset", "field": 'Gene to Phenotype', "value": []},
                {
                    "type": "section-text", "field": 'HPO Terms',
                    // move HPO TERMS HERE HOW???
                    // Need to get it from Clinical History
                    "value": "HPO TERMS TO BE MOVED HERE FROM CLINICAL HISTORY"
                },
            ]
        }, {
            "header": gene.concat(" Molecular Mechanism"),
            "content": [{"type": "section-text", "field": 'Function Overview', "value": []}]
        }, {
            "header": gene.concat(" Function"),
            "content": [{"type": "images-dataset", "field": 'Function', "value": []},]
        }]
      })

      element.sections.push(newGeneSections)
    }
    

    let briefToModelGoalsFields = [];
    let namesOfFieldsToMove = ['Model of Interest', 'Goals', 'Proposed Model/Project']
    element.sections.forEach(section => {
      // print(section)
      const value = Object.values(section)
      
      // print(value)

      if(section.header === 'Brief') {
        section.content.forEach(contentItem => {
          contentItem['type'] = 'section-text';
          if(namesOfFieldsToMove.includes(contentItem.field)) {
            briefToModelGoalsFields.push(contentItem);
          }
        });

        section.content = section.content.filter((contentItem) => {
          return !namesOfFieldsToMove.includes(contentItem.field);
        });
      } else if (section.header === 'Pedigree') {
        section['attachment_field'] = 'Pedigree';
        if(section.content.length == 0) {
          section.content.push[{
            'type': 'images-dataset',
            'field': 'Pedigree',
            'value': []
          }]
        } else {
          print('pedigree section values');
          // take the existing value and put it in the new object format and
          // replace it in the field
        }
      } else {
        section.content.forEach(contentItem => { 
          contentItem['type'] = 'section-text';
        });
      }
      
      // add new sections to sections[] in each element
      // check if field already exists in analyses sections 
      //move field data -- how????

    })

    element.sections.push({
      header: 'Model Goals', 'content': [
       ...briefToModelGoalsFields,
        {'field': 'Existing Collaborations', 'value': [], type: 'section-text'},
        {'field': 'Existing Funding', 'value': [], type: 'section-text'},
      ]
    })

    // print(briefToModelGoalsFields)
    print(element.sections);

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