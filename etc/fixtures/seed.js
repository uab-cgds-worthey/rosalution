// connection URI
const uri = "mongodb://localhost:27017/rosalution_db"

// The default path to the fixtures, can be changed to a script argument in the future
const fixture_path = "/tmp/fixtures"

db = connect(uri)

collections = {
  'analyses': require(`${fixture_path}/initial-seed/analyses.json`),
  'dataset_sources': require(`${fixture_path}/initial-seed/dataset-sources.json`),
  'users': require(`${fixture_path}/initial-seed/users.json`),
}

try {
  console.log(`Connected to MongoDB with URI ${uri}`)

  for( const [collection_name, collection_fixture] of Object.entries(collections) ) {
    db[collection_name].drop()
    print(`Dropping [${collection_name}] collection...`)
    db[collection_name].insertMany(collection_fixture)
    print(`Seeding [${collection_name}] with ${db[collection_name].countDocuments()} documents...`)
  }
  
} catch(err) {
  console.log(err.stack)
}