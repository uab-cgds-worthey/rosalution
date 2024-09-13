const usage = `
mongosh /tmp/database/create-annotation-manifests.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/create-annotation-manifest.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/create-annotation-manifest.js
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
  'Protein Expression': 'Human_Gene_Expression',
}

let yourDate = new Date()
yourDate.toISOString().split('T')[0]

version = {
  'rest': 'rosalution-temp-manifest-00',
  'rosalution': 'rosalution-temp-manifest-00',
  'date': 'rosalution-temp-manifest-00',
}


usernameMapping = {
  'amoss01': '00bqd0d6r0dqpwptyuo8p6h3mnnumzee',
  'afoksin': 'h3bnr2uh1bo4oe0cs1rdyh3n5hrg71ej',
  'aeunoant': '00bqd0d6r0dqpwptyuo8p6h3mnnumzee',
}

usersToUpdate = Object.keys(usernameMapping);


try {
  const analyses = db.analyses.find();
  analyses.forEach(element => {
    print(`Creating analysis' '${element.name}' manifest ...`);
    const annotation_configuration = db.annotations_config.find();

    if (!('manifest' in element))
      element['manifest']= []

    annotation_configuration.forEach(dataset => {
      dataset_name = dataset['data_set']
      if (element.manifest.some(e => dataset_name in e)){
        print("Dataset already in manifest", dataset_name)
        return
      }

      dataset_manifest = {
      }
      version_string = version[config.versioning_type]
      dataset_manifest[dataset_name] = {
        'data_source': dataset['data_source'],
        'version': 'rosalution-temp-manifest-00',
      }
      element['manifest'].push(dataset_manifest)
    });
    print(element['manifest'])
    const updated = db.analyses.updateOne(
      {'_id': element._id},
      {'$set': element}
    )
    print(updated)
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
