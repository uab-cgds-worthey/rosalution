const usage = `
mongosh /tmp/fixtures/add-user.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/update-file-anntation.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/update-file-anntation.js
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

const annotationImageSections = [
    'Gene Homology/Multi-Sequence allignment',
    'Protein Expression',
    'Modelability',
    'Druggability'
]

const oldGeneHomologyKey = 'Gene Homology/Multi-Sequence allignment';
const newGeneHomologyKey = 'Gene Homology/Multi-Sequence Alignment';

try {
    const genomicUnits = db.genomic_units.find();

    genomicUnits.forEach(element => {
        element.annotations.forEach(annotation => {
            const keys = Object.keys(annotation)
            const found = annotationImageSections.some(r => keys.includes(r));
            if(found) {
                annotation[keys[0]].forEach(elem => {
                    const newValue = [{file_id: elem.value, created_date: elem.version}];
                    elem.value = newValue;
                });
                if(keys[0] == 'Gene Homology/Multi-Sequence allignment') {
                    delete Object.assign(annotation, {[newGeneHomologyKey]: annotation[oldGeneHomologyKey] })[oldGeneHomologyKey];
                }
                console.log(element)
                db.genomic_units.update(
                    {'_id': element._id},
                    {'$set': element},
                )
            }
        })
    });
} catch (err) {
    console.log(err.stack);
    console.log(usage);
    quit(1);
}