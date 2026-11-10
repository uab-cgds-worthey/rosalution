const usage = `
mongosh --eval 'var rapidScreenAnalysis=""' /tmp/administration/transform-to-cpam-rapid-review-analysis.js

Script Options:
    help : Bool : Optional
        - If True print this help message
    rapidScreenAnalysis : String : Required

Run mongosh help for mongosh connection and authentication usage.

Example:

    mongosh --host localhost --port 27017 --eval 'var help=True;' /tmp/administration/transform-to-cpam-rapid-review-analysis.js

    docker exec -it <rosalution_db_container> mongosh --eval 'var rapidScreenAnalysis="PCS2026027 (GRIN2D)"' /tmp/administration/transform-to-cpam-rapid-review-analysis.js
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

if(typeof rapidScreenAnalysis === 'undefined' || typeof rapidScreenAnalysis !== 'string' || rapidScreenAnalysis == '') {
    print('rapidScreenAnalysis needs to be defined and must be a string');
    print(usage);
    quit(1);
}

function doesSectionExist(sections, sectionName) {
    for(section of sections) {
        if(section.header == sectionName) {
            return true;
        }
    }
    return false;
}

function doesFieldExist(section, fieldName) {
    for(row of section['content']) {
        if(row['field'] == fieldName) {
            return true;
        }
    }
    return false;
}

print(`Converting ${rapidScreen}'s Analysis from Standard to Rapid Screening Analysis...`)

const fieldsToIncludeBySection = {
    'Brief': ['Nominator', 'Participant', 'Decision', 'Patient phenotype', 'Family history'],
    'Rapid Screen Goals': ['Recommended screen', 'Confidence', 'Goals', 'Suspected mechanism'],
    'Rapid Screen Fit': ['Xenopus (oocyte) overexpression fitness', 'Xenopus (oocyte) overexpression', 'Zebrafish crispant fitness', 'Zebrafish crispant'],
    'Rapid Screen Impact': ['Positive', 'Negative']
}

const sectionTextField = {
    "type":"section-text",
    "field":"",
    "value":[]
}

function fieldHasContent(fieldValueList) {
     for (value of fieldValueList) {
        if (typeof value != 'string') {
            return true;
        }

        if(value.trim().length != 0) {
            return true;
        }
     }

     return false;
}

function doesSectionHaveContent(section) {
    for (row of section['content']) {
        if(fieldHasContent(row['value'])) {
            return true
        }
    }

    return false
}

function createSection(headerName, fieldNames) {
    return {
        header: headerName,
        content: fieldNames.map((fieldName) => {
             return {
                type: 'section-text',
                field: fieldName,
                value: []
             }
        })
    }
}

// Getting the database driver for mongo
db = db.getSiblingDB(databaseName)

// Getting the analysis and inserting the new sections
try {
    var analysis = db.analyses.findOne({name: rapidScreenAnalysis})
    print(`Found '${rapidScreenAnalysis}' in mongodb...`)

    var index = 0;

    var sectionsToRemove = [];
    var foundSections = [];

    for(sectionIndex in analysis.sections) {
        var fieldsToAdd = [];
        const headerName = analysis.sections[sectionIndex].header
        if(headerName in fieldsToIncludeBySection) {
            foundSections.push(headerName)
            print(`Transforming ${headerName} Section ...`)
            if(doesSectionHaveContent(analysis.sections[sectionIndex])) {
                print(`Transforming ${headerName} Section ... aborted, section contains content`)
                continue;
            }
            print(`Transforming ${headerName} Section ... complete`)
            analysis.sections[sectionIndex] = createSection(headerName, fieldsToIncludeBySection[headerName])
        } else {
            print(`Section ${headerName}, flagging for removal...`)
            if(doesSectionHaveContent(analysis.sections[sectionIndex])) {
                print(`Section ${headerName}, has content, not removing...`)
            } else {
                sectionsToRemove.push(headerName)
            }
        }
    }
    print(`Sections to remove [${sectionsToRemove}]`)
    if( sectionsToRemove.length > 0 ) {
        analysis.sections = analysis.sections.filter((section) => {
            const sectionNameToCheck = section.header
            const isSectionFlaggedForRemoval = sectionsToRemove.includes(sectionNameToCheck)
            return isSectionFlaggedForRemoval == false
        });
    }

    for(sectionName in fieldsToIncludeBySection) {
        if (foundSections.includes(sectionName)) {
            continue;
        }

        analysis.sections.push(createSection(sectionName, fieldsToIncludeBySection[sectionName]))
    }

    print(`Writing to mongodb...`)
    db.analyses.updateOne({'_id': analysis._id}, {'$set': analysis})

    print(`Success! Done.`)
} catch(e) {
    console.log(e.stack);
    console.log(usage);
    quit(1);
}
