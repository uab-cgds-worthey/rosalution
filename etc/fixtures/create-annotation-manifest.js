const usage = `
mongosh /tmp/database/create-annotation-manifests.js
    Script Options:
        help: if true print this help message
        overwrite: replace the existing analysis' annotation manifest
        databaseName: different name of the database if needed

    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --file /tmp/fixtures/create-annotation-manifest.js overwrite --eval="databaseName='rosalution_db'"
    docker exec -it <rosalution_db_container> mongosh --file /tmp/fixtures/create-annotation-manifest.js overwrite --eval="databaseName='rosalution_db'"
`

overwrite = process.argv.includes('overwrite')
help = process.argv.includes('help')

if (help) {
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
  'Protein Expression': 'Human_Gene_Expression',
}

let yourDate = new Date()
yourDateString = yourDate.toISOString().split('T')[0].split('T')[0]

versionMapping = {
  'rosalution': 'rosalution-manifest-00',
  'date': yourDateString,
  'Ensembl': 112,
  'Alliance Genome': '7.3.0',
  'Alliance genome': '7.3.0',
}

function createAnalysisManifestEntry(incomingDataset) {
  datasetManifest = {
  }

  datasetName = incomingDataset['data_set']
  versionType = incomingDataset['versioning_type']
  annotationSource = incomingDataset['data_source']
  versionString =  versionType in versionMapping ? versionMapping[versionType] : versionMapping[annotationSource]
  datasetManifest[datasetName] = {
    'data_source': incomingDataset['data_source'],
    'version': versionString,
  }

  return datasetManifest
}

function getAnalysisGenomicUnits(genomicUnits) {
  function getHgvsVariants(variants) {
    return variants.flatMap( variant => [variant.hgvs_variant && { 'hgvs_variant': variant.hgvs_variant}]);
  }
  return genomicUnits.flatMap( unit => ('variants' in unit ? [{'gene': unit['gene'] }, ...getHgvsVariants(unit['variants'])]: unit['gene']))
}

function getVersionFromManifest(manifest, datasetName) {
  const found = manifest.find((config) => Object.hasOwn(config, datasetName))
  if(!found)
    return undefined
  return found[datasetName].version
}

try {
  const analyses = db.analyses.find();
  analyses.forEach(element => {
    print(`Creating analysis: '${element.name}' manifest...`);
    const annotation_configuration = db.annotations_config.find();

    if( overwrite ) {
      element['manifest']= []
    }


    annotation_configuration.forEach(dataset => {
      datasetName = dataset['data_set']
      datasetManifest = createAnalysisManifestEntry(dataset)

      if (!overwrite && element.manifest.some(e => datasetName in e)){
        print("Dataset already in manifest", datasetName)
        return
      }
      element['manifest'].push(datasetManifest)

    });

    analysisGenomicUnits = getAnalysisGenomicUnits(element['genomic_units'])
    analysisGenomicUnits.forEach((genomicUnit) => {
      // db.genomic_units.findOne({'hgvs_variant': 'NM_001360016.2:c.563C>T'});
      // db.genomic_units.findOne({'gene': 'VMA21'});
      genomicUnitDocument = db.genomic_units.findOne(genomicUnit)

      genomicUnitDocument.annotations.forEach( annotation =>  {
        for (const annotationUnitDataset of Object.keys(annotation)) {
          annotation[annotationUnitDataset].forEach(annotationUnit => {
            annotationUnit.version = getVersionFromManifest(element['manifest'], annotationUnitDataset)
          })
        }
      });

      if( Object.hasOwn(genomicUnitDocument, 'transcripts')) {
        genomicUnitDocument.transcripts.forEach( transcript =>  {
          transcript.annotations.forEach((annotation) => {
            for (const annotationUnitDataset of Object.keys(annotation)) {
              annotation[annotationUnitDataset].forEach(annotationUnit => {
                annotationUnit.version = getVersionFromManifest(element['manifest'], annotationUnitDataset)
              }); 
            }
          });
        });
      }
      db.genomic_units.updateOne(
        {'_id': genomicUnitDocument._id},
        {'$set': genomicUnitDocument}
      )
    });
    print('Updating analysis: ' + element.name + "...")
    const updated = db.analyses.updateOne(
      {'_id': element._id},
      {'$set': element}
    )
    result_text = updated.modifiedCount == 1 ? 'Success': 'Existed'
    print('Updating analysis: ' + element.name + "..." + result_text)
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
