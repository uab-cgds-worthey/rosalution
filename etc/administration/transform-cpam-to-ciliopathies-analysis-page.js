const usage = `
mongosh --eval 'var ciliAnalysis=""' /tmp/administration/transform-cpam-to-ciliopathies-analysis-page.js

Script Options:
    help : Bool : Optional
        - If True print this help message
    ciliAnalysis : String : Required

Run mongosh help for mongosh connection and authentication usage.

Example:

    mongosh --host localhost --port 27017 --eval 'var help=True;' /tmp/administration/transform-cpam-to-ciliopathies-analysis-page.js

    docker exec -it <rosalution_db_container> mongosh --eval 'var ciliAnalysis="CILI_2_5K ARMC9_L510V"' /tmp/administration/transform-cpam-to-ciliopathies-analysis-page.js
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

if(typeof ciliAnalysis === 'undefined' || typeof ciliAnalysis !== 'string' || ciliAnalysis == '') {
    print('ciliAnalysis needs to be defined and must be a string');
    print(usage);
    quit(1);
}

function doesSectionExist(sections, sectionName) {
    for(section in sections) {
        if(sections[section].header == sectionName) {
            return true;
        }
    }
    return false;
}

function doesFieldExist(section, fieldName) {
    for(row in section['content']) {
        if(section['content'][row]['field'] == fieldName) {
            return true;
        }
    }
    return false;
}

print(`Converting ${ciliAnalysis}'s Analysis View from CPAM to Ciliopathies...`)

// New Ciliopathy specific fields

const databaseTextField = {
    "type":"section-text",
    "field":"Database",
    "value":[]
}

const patientRelatedVariantEvidenceField = {
    "type": "section-attachment",
    "field": "Patient Related Variants",
    "value": []
}

const resourcesSection = {
    "header": "Resources",
    "content": [
        {
            "type": "section-text",
            "field": "Purchased Antibody Catalog #",
            "value": []
        },
        {
            "type": "section-text",
            "field": "Physical Resources",
            "value": []
        }
    ]
}

const reportingSection = {
    "header": "Reporting",
    "content": [
        {
            "type": "section-attachment",
            "field": "Benchling",
            "value": []
        }
    ]
}

// Getting the database driver for mongo
db = db.getSiblingDB(databaseName)

// Getting the analysis and inserting the new sections
// Note: This will insert the fields twice if run twice
try {
    var analysis = db.analyses.findOne({name: ciliAnalysis})
    print(`Found ${ciliAnalysis} in mongodb...`)

    var index = 0;

    for(section in analysis.sections) {        
        if(analysis.sections[section].header == 'Brief') {

            if (!doesFieldExist(analysis.sections[section], databaseTextField['field'])) {
                print(`Inserting the Database text field into the Brief section...`)
                analysis.sections[section]['content'].splice(1, 0, databaseTextField);
            } else {
                print(`Database text field already exists in the Brief section...`)
            }

            if (!doesFieldExist(analysis.sections[section], patientRelatedVariantEvidenceField['field'])) {
                print(`Inserting the Patient Related Variants Evidence field into the Brief section...`)
                analysis.sections[section]['content'].push(patientRelatedVariantEvidenceField)
            } else {
                print(`Patient Related Variants Evidence field already exists in the Brief section...`)
            }
        }
    }

    if ( !doesSectionExist(analysis.sections, resourcesSection['header']) ) {
        for(section in analysis.sections) {
            if(analysis.sections[section].header == 'Pedigree') {
                console.log(`Section #: ${section}, Header: ${analysis.sections[section].header}`)
                print(`Inserting the Resources section into the analysis...`)
                analysis.sections.splice(section, 0, resourcesSection)
                break;
            }
        }   
    } else {
        print(`Resources section already exists in the analysis...`)
    }

    if ( !doesSectionExist(analysis.sections, reportingSection['header']) ) {
        for(section in analysis.sections) {
            if(analysis.sections[section].header == 'Model Goals') {
                console.log(`Section #: ${section}, Header: ${analysis.sections[section].header}`)
                print(`Inserting the Reporting section into the analysis...`)
                analysis.sections.splice(section + 1, 0, reportingSection)
                break;
            }
        }
    } else {
        print(`Reporting section already exists in the analysis...`)
    }

    print(`Writing to mongodb...`)
    db.analyses.updateOne({'_id': analysis._id}, {'$set': analysis})

    print(`Success! Done.`)
} catch(e) {
    console.log(e.stack);
    console.log(usage);
    quit(1);
}
