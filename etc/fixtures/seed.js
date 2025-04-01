// connection URI
const uri = 'mongodb://localhost:27017/rosalution_db';

// The default path to the fixtures, can be changed to a script argument in the future
const fixturePath = '/tmp/fixtures';

// This JavaScript executes within a mongosh shell making 'connect' is implicitly available
const db = connect(uri); // eslint-disable-line no-undef

const collections = {
  // 'analyses': require(`${fixturePath}/initial-seed/analyses.json`),
  'annotations_config': require(`${fixturePath}/initial-seed/annotations-config.json`),
  // 'users': require(`${fixturePath}/initial-seed/users.json`),
  'genomic_units': require(`${fixturePath}/initial-seed/genomic-units.json`),
};

try {
  console.log(`Connected to MongoDB with URI ${uri}`);

  for ( const [collectionName, collectionFixture] of Object.entries(collections) ) {
    db[collectionName].drop();
    print(`Dropping [${collectionName}] collection...`);
    db[collectionName].insertMany(collectionFixture);
    print(`Seeding [${collectionName}] with ${db[collectionName].countDocuments()} documents...`);
  }

  print(`Dropping [fs.chunks] & ['fs.files'] collections for GridFS buckets...`);
  db['fs.chunks'].drop();
  db['fs.files'].drop();
} catch (err) {
  console.log(err.stack);
}
