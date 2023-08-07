const fs = require('fs');

const inputPath = `/tmp/fixtures/simplifiedDittoScores.csv`
var dittoScoreList = [];

var csvData = fs.readFileSync(inputPath)
    .toString() // convert Buffer to string
    .split('\n') // split string to lines
    .map(e => e.trim()) // remove white spaces for each line
    .map(e => e.split(',').map(e => e.trim())); // split each line to array

console.log(csvData)

for(let i = 0; i < csvData.length; i++) {
    if(csvData[i][0] == 'HGVS')
        continue;

    dittoScore = {
        hgvs_variant: '',
        annotation: {
            DITTO: []
        },
    }

    const ditto_annotation = { data_source: 'DITTO', version: '', value: 0, }

    dittoScore.hgvs_variant = csvData[i][0]
    ditto_annotation.value = csvData[i][1]

    dittoScore.annotation.DITTO.push(ditto_annotation);

    dittoScoreList.push(dittoScore);
}

db = db.getSiblingDB('rosalution_db');

try {
    const genomic_units = db.genomic_units.find();

    if(genomic_units.size() == 0)
        throw new Error(`No genomic units found in ${databaseName}. Aborting.`)

    let newUnits = []
    genomic_units.forEach(unit => {
        if(unit['hgvs_variant'] !== undefined) {
            for(score in dittoScoreList) {
                if(dittoScoreList[score].hgvs_variant == unit.hgvs_variant) {
                    console.log(unit.hgvs_variant)
                    unit.annotations.push(dittoScoreList[score].annotation)
                    newUnits.push(unit);
                }
            }
        }
    })

    console.log(newUnits)    

    newUnits.forEach(unit => {db.genomic_units.updateOne({'_id': unit._id}, {'$set': unit})});
} catch (err) {
    console.log(err.stack);
    console.log(usage);
    quit(1);
}

console.log(`Ditto scores added!`);