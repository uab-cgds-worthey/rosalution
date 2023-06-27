/* mongosh /tmp/fixtures/remove-automatic-annotations.js */

const databaseName = 'rosalution_db';

db = db.getSiblingDB(databaseName);

try {
    const genomic_units = db.genomic_units.find();
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

    newUnits.forEach(unit => {
        unit.annotations = unit.annotations.filter(object => Object.keys(object).length !== 0);
    });

    // console.log(newUnits)

    newUnits.forEach(unit => {
        // console.log(unit._id);
        db.genomic_units.updateOne(
            {'_id': unit._id},
            {'$set': unit},
        )
    })
} catch (err) {
    console.log(err.stack);
    console.log(usage);
    quit(1);
}