const usage = `
mongosh --eval 'var cpamAnalysis="";var modelSystem=""' /tmp/fixtures/migrations/migrate-insert-animal-model-systems.js

    Script Options:
        help : Bool : Optional
            - If True print this help message
        cpamAnalysis : String : Required
        modelSystem : String : Required
            - Mus musculus (Mouse) Model System
            - Danio rerio (Zebrafish) Model System
            - Rattus norvegicus (Rat) Model System
            - Xenopus laevis (Frog) Model System
            - C. elegans (Roundworm) Model System
    
    Run mongosh help for mongosh connection and authentication usage.

    Example:

    mongosh --host localhost --port 27017 --eval 'var help=True;' /tmp/fixtures/migrations/migrate-insert-animal-model-systems.js

    docker exec -it <rosalution_db_container> mongosh --eval 'var cpamAnalysis="CPAM0002";var modelSystem="Mus musculus (Mouse) Model System"' /tmp/fixtures/migrations/migrate-insert-animal-model-systems.js
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

if(typeof cpamAnalysis === 'undefined' || typeof cpamAnalysis !== 'string' || cpamAnalysis == '') {
    print('cpamAnalysis needs to be defined and must be a string');
    print(usage);
    quit(1);
}

if(typeof modelSystem === 'undefined' || typeof modelSystem !== 'string' || modelSystem == '') {
    print('modelSystem needs to be defined and must be a string');
    print(usage);
    quit(1);
}

print(`Adding ${modelSystem} to ${cpamAnalysis}...`)

db = db.getSiblingDB(databaseName)

const animalModelSystemSection = {
    "header": modelSystem,
    "content": [
        {
            "type": "section-text",
            "field": "Mutation",
            "value": []
        },
        {
            "type": "section-text",
            "field": "Pathogenicity Test",
            "value": []
        },
        {
            "type": "section-text",
            "field": "Design",
            "value": []
        },
        {
            "type": "section-text",
            "field": "Founder Screening/Expansion",
            "value": []
        },
        {
            "type": "section-text",
            "field": "Screening",
            "value": []
        },
        {
            "type": "section-text",
            "field": "History",
            "value": []
        },
        {
            "type": "section-text",
            "field": "Diagnoses",
            "value": []
        },
        {
            "type": "section-text",
            "field": "Remarks",
            "value": []
        },
        {
            "type": "supporting-evidence",
            "field": "Vetrinary Pathology Imaging",
            "value": []
        },          
        {
            "type": "supporting-evidence",
            "field": "Vetrinary Pathology Report",
            "value": []
        }
    ]
}

try {
    var analysis = db.analyses.findOne({name: cpamAnalysis})
    print(`Found ${cpamAnalysis} in mongodb...`)
    var index = 0;

    for(section in analysis.sections) {
        if(analysis.sections[section].header == 'Pedigree') {
            index = section
            break;
        }
    }

    print(`Inserting '${modelSystem}' section into the analysis...`)
    analysis.sections.splice(index, 0, animalModelSystemSection)

    print(`Writing to mongodb...`)
    db.analyses.updateOne({'_id': analysis._id}, {'$set': analysis})

    print(`Success! Done.`)
} catch(e) {
    console.log(e.stack);
    console.log(usage);
    quit(1);
}

