const usage = `
mongosh /tmp/fixtures/migrations/remove-empty-annotations.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/migrations/remove-empty-annotations.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/remove-empty-annotations.js
`

if (typeof databaseName === 'undefined') {
    databaseName = "rosalution_db";
}

db = db.getSiblingDB(databaseName);

const datasetsToResolve = {
    'gene': [
        'Zebrafish_Alliance_Genome_Automated_Summary',
        'Zebrafish_Alliance_Genome_ZFIN_Summary',
        'Zebrafish_Alliance_Genome_Models',
        'ZEBRAFISH_SUMMARY_ALLIANCE_GENOME_CACHE',
        'MOUSE_SUMMARY_ALLIANCE_GENOME_CACHE',
        'RAT_SUMMARY_ALLIANCE_GENOME_CACHE',
        'Mouse_Alliance_Genome_Models',
        'Mouse_Alliance_Genome_MGI_Summary',
        'Mouse_Alliance_Genome_Automated_Summary',
        'Rat_Alliance_Genome_Models',
        'Rat_Alliance_Genome_RGD_Summary',
        'Rat_Alliance_Genome_Automated_Summary',
    ]
}


try {
  const analyses = db.analyses.find({'name': 'CPAM0084duplicate'});
//   const analyses = db.analyses.find();
  analyses.forEach(element => {
    print(`Migrating analysis ${element.name} -----`)

    const unitsList = []
    element.genomic_units.forEach(unit=> {
        if( 'gene' in unit ) {
            unitsList.push({'gene': unit['gene']});
        }
    });

    element.manifest.filter( manifestEntry => {
        return datasetsToResolve['gene'].some(dataset => Object.keys(manifestEntry).includes(dataset));
    }).forEach( manifestEntry => {
        Object.keys(manifestEntry).forEach( dataset => {
            let found = true;
            unitsList.map( omicUnit => {
                // print(omicUnit)
                // print(manifestEntry)
                /**
                 * Example Find query for dataset
                 * {
                 *   gene: 'DLG4',
                 *   'annotations.Zebrafish_Zebrafish_Information_Network_url': { '$exists': true },
                 *   'annotations.Zebrafish_Zebrafish_Information_Network_url.data_source': 'Alliance Genome',
                 *   'annotations.Zebrafish_Zebrafish_Information_Network_url.version': '8.2.0'
                 * }
                 */
                const findQuery = {
                    ...omicUnit
                }
                const annotationExist = `annotations.${dataset}`;
                findQuery[annotationExist] = {$exists: true};
                findQuery[`annotations.${dataset}.data_source`] =  manifestEntry[dataset]['data_source'];
                findQuery[`annotations.${dataset}.version`] =  manifestEntry[dataset]['version'];
                // print(`Analysis "${element.name}" - ${dataset}: Find Query`)
                // print(findQuery)
                return findQuery
            }).forEach(findQuery => {
                
                /**
                 * Example Projection for Find Query
                 * {
                 *   gene: 1,
                 *   'annotations.Zebrafish_Zebrafish_Information_Network_url.$': 1
                 * }
                 */
                const projection = Object.keys(findQuery).reduce( (accumulator, key) => {
                    if( (key.includes('.data_source') || key.includes('.version')) ) {
                        return accumulator;
                    }
                    if (!key.includes('annotations')) {
                        accumulator[key] = 1
                        return accumulator;
                    }
                    const singleItem = `${key}.$`
                    accumulator[singleItem] = 1;
                    return accumulator
                }, {})

                const foundOmicUnit = db.genomic_units.findOne(findQuery, projection);

                if( !foundOmicUnit ) {
                    found = false;
                    // print(`Analysis "${element.name}" - ${findQuery['gene']} - ${dataset}: Not Found`)
                } else {
                    // print(`Analysis "${element.name}" - ${findQuery['gene']} - ${dataset}: Found`)
                }
                // else {
                //     print(`Analysis "${element.name}" - ${dataset}: Found`)

                //     foundOmicUnit.annotations.forEach(annotation => {
                //         const isDatasetEmpty = annotation[dataset].filter(annotationEntry => {
                //             if( Array.isArray(annotationEntry['value'])) {
                //                 return annotationEntry['value'].length > 0
                //             }
                //             return annotationEntry['value'] != null ||
                //                 annotationEntry['value'] != undefined ||
                //                 annotationEntry['value'] != ""
                //         });
                //         if (!isDatasetEmpty.length) {
                //             print(`Analysis "${element.name}" - ${dataset}: Found but Empty`)
                //             print(findQuery)
                //             // print('projection used')
                //             print(projection)
                //             print(foundOmicUnit)
                //         }
                //     })
                // }
            });
            if (!found) {
                print(`Analysis "${element.name}" - ${dataset}: Not Found for One to Many omic units`)
                const filter = {
                    'name': element.name,
                }
                filter[`manifest.${dataset}`] = {$exists: true}
                const existsCondition = {}
                existsCondition[dataset] = {$exists: true}
                const update = {
                    '$pull': {'manifest': existsCondition }
                }
                db.analyses.findOneAndUpdate(filter, update)
                print(`Analysis "${element.name}" - ${dataset}: Removed`)
            }
        });
        // print('----------------------------------------------------------------------------------------');
    });
})

//     let caseUpdated = false;
//     element.sections.forEach(section => {
//       if ( ['Pedigree', 'Gene To Phenotype', 'Function'].some((value) => {
//         return section.header.includes(value);
//       }) && !section.hasOwnProperty('attachment_field') ) {        
//         section['attachment_field'] = section.header;
//         caseUpdated = true;
//         print(section);
//       }
      
//       if ( section.header.includes('Gene to Phenotype') ) {
//         const replaced = section.header.replace('to', 'To');
//         section.header = replaced;
//         section['attachment_field'] = replaced;
//         section.content.forEach((row) => {
//           if(row.field.includes('Gene to Phenotype')){
//             row.field = replaced;
//           }
//         })
//         caseUpdated = true;
//         print(section);
//       }
//     })
    
//     if(caseUpdated) {
//       print(`  ${element.name} updated...`)
//     }

//     // update       
//     db.analyses.update(
//       {'_id': element._id},
//       {'$set': element}
//     )
//     print(`Updated ${element.name} -----`)
//   });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}

// try {
//   const genomicUnits = db.genomic_units.find();
//   genomicUnits.forEach(element => {
//     element.annotations.forEach(annotation => {
//         const annotation_name = Object.keys(annotation)
        
//         if (annotationSectionsRename[annotation_name]) {
//           Object.assign(annotation, {[annotationSectionsRename[annotation_name]]: annotation[annotation_name]})
//           delete annotation[annotation_name]
          
//           db.genomic_units.update(
//             {'_id': element._id},
//             {'$set': element}
//           )
//         }
//     })
//   });
// } catch (err) {
//   console.log(err.stack);
//   console.log(usage);
//   quit(1);
// }
