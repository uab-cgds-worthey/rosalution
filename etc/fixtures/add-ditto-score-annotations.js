// docker exec -it rosalution-rosalution-db-1 mongosh --eval "var dittoScoreCSVPath='/tmp/fixtures/example.csv'" /tmp/add-ditto-score-annotations.js

const usage = `
mongosh /tmp/add-ditto-score-annotations.js

    Script Options:
        help                Bool    If True prints this help message
        databaseName        String  Mongo database name to use                       default: rosalution_db
        dittoScoreCSVPath   String  File to read ditto score to genomic unit mapping

    Run mongosh help for mongosh connection and authentication usage.

    Examples:
    mongosh --eval "var dittoScoreCSVPath='/tmp/fixtures/example.csv'" /tmp/add-ditto-score-annotations.js
    mongosh --host localhost --port 27017 --eval "var dittoScoreCSVPath='/tmp/fixtures/example.csv'; databaseName='<database_name>'" /tmp/add-ditto-score-annotations.js
`;

const fs = require('fs');

if (help == true) {
    print(usage);
    quit(1);
}

// const dittoScoreCSV = `/tmp/fixtures/simplifiedDittoScores.csv`

// Checking the ditto score csv path
if (typeof dittoScoreCSVPath === 'undefined') {
    dittoScoreCSVPath = "/tmp/fixtures/example-adding-users.json";
} else if (typeof dittoScoreCSVPath !== 'string') {
    print("dittoScoreCSV must be a string containing file path");
    quit(1);
}

// Checking if custom databaseName string
if (typeof databaseName === 'undefined') {
    databaseName = "rosalution_db";
} else if (typeof databaseName !== 'string') {
    print("databaseName must be a string");
    quit(1);
}

db = db.getSiblingDB(databaseName);

var dittoScoreList = [];

var csvData = fs.readFileSync(dittoScoreCSVPath)
    .toString() 
    .split('\n') 
    .map(e => e.trim()) 
    .map(e => e.split(',').map(e => e.trim())); 

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

try {
    let count = 0;

    for(score in dittoScoreList) {
        const genomic_unit = db.genomic_units.findOne({ hgvs_variant: dittoScoreList[score].hgvs_variant})

        if(genomic_unit == null)
            continue;
        
        console.log(`Adding Ditto Score: ${dittoScoreList[score].annotation.DITTO[0].value} to genomic unit: ${dittoScoreList[score].hgvs_variant}`)

        genomic_unit.annotations.push(dittoScoreList[score].annotation)
        db.genomic_units.updateOne({'_id': genomic_unit._id}, {'$set': genomic_unit})
        count++;
    }

    console.log(`${count} Ditto scores added! Exiting.`);
} catch (err) {
    console.log(err.stack);
    console.log(usage);
    quit(1);
}

