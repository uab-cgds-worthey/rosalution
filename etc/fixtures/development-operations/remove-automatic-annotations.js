const usage = `
Script usage for 'remove-automatic-annotations.js':

mongosh /tmp/fixtures/remove-automatic-annotations.js
    Script Options:
        help            If true, prints this message.
        databaseName    Database name to use - default: rosalution_db
    
    For mongosh connection and authentication usage, please run: mongosh help

    Examples:
        mongosh --host localhost --port 27017 /tmp/fixtures/remove-automatic-annotations.js
        mongosh --host localhost --port 27017 --eval "help=true;databaseName='your_db_name'" /tmp/fixtures/remove-automatic-annotations.js 
`

if(help == true) {
    print(usage);
    quit(1);
}

if(typeof databaseName == 'undefined')
    databaseName = 'rosalution_db';
else if(typeof databaseName !== 'string') {
    print("databaseName must be a string");
    quit(1);
}

db = db.getSiblingDB(databaseName);

console.log(`Removing non-manual annotations from ${databaseName}...`);

try {
    const genomic_units = db.genomic_units.find();

    if(genomic_units.size() == 0)
        throw new Error(`No genomic units found in ${databaseName}. Aborting.`)

    const newUnits = [];
    genomic_units.forEach(unit => {
        unit.annotations.forEach(annotation => {
            for(const [key, value] of Object.entries(annotation)) {
                annotation[key] = annotation[key].filter(object => object['data_source'] == 'rosalution-manual')
                if(annotation[key].length < 1)
                    delete annotation[key];
            }
        })

        newUnits.push(unit);
    });

    newUnits.forEach(unit => {unit.annotations = unit.annotations.filter(object => Object.keys(object).length !== 0)});
    newUnits.forEach(unit => {db.genomic_units.updateOne({'_id': unit._id}, {'$set': unit})});

} catch (err) {
    console.log(err.stack);
    console.log(usage);
    quit(1);
}

console.log(`Annotation removal complete.`);