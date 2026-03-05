// connection URI
const uri = 'mongodb://localhost:27017/rosalution_db';

// The default path to the fixtures
const fixturePath = '/tmp/fixtures';

const db = connect(uri); // eslint-disable-line no-undef

const loadBson = function(path) {
  const raw = fs.readFileSync(path, 'utf8');
  let docs = EJSON.parse(raw);
  return Array.isArray(docs) ? docs : [docs];
};


const collections = {
  'projects': loadBson(`${fixturePath}/initial-seed/projects.json`),
  'analyses': loadBson(`${fixturePath}/initial-seed/analyses.json`),
  'annotations_config': require(`${fixturePath}/initial-seed/annotations-config.json`),
  'users': loadBson(`${fixturePath}/initial-seed/users.json`),
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
