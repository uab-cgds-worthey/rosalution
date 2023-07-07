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
    print(`Migrating case ${element.name} -----`)

    let briefToModelGoalsFields = [];
    let namesOfFieldsToMove = ['Model of Interest', 'Goals', 'Proposed Model/Project']
    let HPOTermsValues = [];
    element.sections.forEach(section => {

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
        print(`  - Removing sections from Brief to go to Model Goals...`)
      } else if (section.header === 'Pedigree') {
        section['attachment_field'] = 'Pedigree';
        if(section.content.length == 0) {
          section.content.push[{
            'type': 'images-dataset',
            'field': 'Pedigree',
            'value': []
          }]
          print(`  - Creating image dataset for empty pedigree...`)
        } else {
          let updatedContent = []
          section.content.forEach((image) => {
            let newValues = [];
            image.value.forEach(imageId => {
              newValues.push( {file_id: imageId});
            });
            updatedContent.push({
              type: 'images-dataset',
              field: section.header,
              value: newValues
            })
          })
          print(`  - Migrateing image dataset for for pedigree...`)
          section.content = updatedContent
         }
      } else if (section.header === 'Clinical History') { 
        section.content.forEach(contentItem => {
          contentItem['type'] = 'section-text';
          if(contentItem.field === 'HPO Terms') {
            HPOTermsValues = contentItem.value;
          }
        });

        section.content = section.content.filter((contentItem) => {
          return !contentItem.field === 'HPO Terms';
        });
        print(`  - Removing HPO Terms From Clinical History...`)
      } else {
        if(!['Function', 'Molecular', 'Gene'].some(element => section.header.includes(element))) {
          section.content.forEach(contentItem => { 
            contentItem['type'] = 'section-text';
          });
        }
      }
    })

    // Adding new sections for each gene
    genes = []
    element.genomic_units.forEach(unit => {
      if (unit.gene) {
        genes.push(unit.gene)
      }
    })

    if (genes.length > 0) {
      genes.forEach(gene => {
        newGeneSections = [{
            "header": gene.concat(" Gene to Phenotype"), 
            "attachment_field": gene.concat(" Gene to Phenotype"),
            "content": [
                {"type": "images-dataset", "field": gene.concat(" Gene to Phenotype"), "value": []},
                {
                    "type": "section-text", "field": 'HPO Terms',
                    "value": HPOTermsValues
                },
            ]
        }, {
            "header": gene.concat(" Molecular Mechanism"),
            "content": [{"type": "section-text", "field": gene.concat(" Molecular Mechanism"), "value": []}]
        }, {
            "header": gene.concat(" Function"),
            "attachment_field": gene.concat(" Function"),
            "content": [{"type": "images-dataset", "field": gene.concat(" Function"), "value": []},]
        }]
        print(`  - Adding Moving HPO terms from Clinical History...`)
        print(`  - Adding new sections for ${gene}...`)
        element.sections.push(...newGeneSections)
      })
    }

    // Adding model goals section
    element.sections.push({
      header: 'Model Goals', 'content': [
       ...briefToModelGoalsFields,
        {'field': 'Existing Collaborations', 'value': [], type: 'section-text'},
        {'field': 'Existing Funding', 'value': [], type: 'section-text'},
      ]
    })
    print(`  - Copyed sections from brief into Model Goals...`)

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