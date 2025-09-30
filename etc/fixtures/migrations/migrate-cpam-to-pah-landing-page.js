const usage = `
mongosh --eval 'var pahAnalysis=""' /tmp/fixtures/migrations/migrate-cpam-to-pah-landing-page.js

Script Options:
    help : Bool : Optional
        - If True print this help message
    pahAnalysis : String : Required

Run mongosh help for mongosh connection and authentication usage.

Example:

    mongosh --host localhost --port 27017 --eval 'var help=True;' /tmp/fixtures/migrations/migrate-cpam-to-pah-landing-page.js

    docker exec -it <rosalution_db_container> mongosh --eval 'var pahAnalysis="PAH AK2_rs752889879"' /tmp/fixtures/migrations/migrate-cpam-to-pah-landing-page.js
`

if (help === true) {
    print(usage);
    quit(1);
}

if (typeof databaseName === 'undefined') {
    databaseName = 'rosalution_db';
} else if (typeof databaseName !== 'string') {
    print('databaseName must be a string');
    print(usage);
    quit(1);
}

if(typeof pahAnalysis === 'undefined' || typeof pahAnalysis !== 'string' || pahAnalysis == '') {
    print('pahAnalysis needs to be defined and must be a string');
    print(usage);
    quit(1);
}

print(`Converting ${pahAnalysis}'s Analysis View from CPAM to PAH...`)

// Getting the database driver for mongo
db = db.getSiblingDB(databaseName)

// Getting the analysis and inserting the new sections
// Note: This will insert the fields twice if run twice
try {
    var analysis = db.analyses.findOne({name: pahAnalysis})
    print(`Found ${pahAnalysis} in mongodb...`)

    var index = 0;

    // console.log(analysis.sections)

    var genes = [];

    // Find genes in analysis
    for(const unit of analysis.genomic_units) {
        if('gene' in unit)
            genes.push(unit.gene);
    }

    for(const gene of genes) {
        let networkImageSection = {
            "header":`${gene} Networks & Interactions`,
            "attachment_field":`${gene} Networks & Interactions`,
            "content":[
                {
                    "type": "images-dataset",
                    "field": `${gene} Networks & Interactions`,
                    "value":[]
                }
            ]
        };

        for(section in analysis.sections) {
            if(analysis.sections[section].header == `${gene} Function`) {
                console.log(`Section #: ${section}, Header: ${analysis.sections[section].header}`)
                console.log(`Inserting '${networkImageSection.header}' into the analysis...'`);
                section++;
                analysis.sections.splice(section, 0, networkImageSection);
                break;
            }
        }
    }

    print(`Writing to mongodb...`)
    db.analyses.updateOne({'_id': analysis._id}, {'$set': analysis})

    print(`Success! Done.`)
} catch(e) {
    console.log(e.stack);
    console.log(usage);
    quit(1);
}
