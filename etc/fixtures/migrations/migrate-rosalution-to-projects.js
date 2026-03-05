const usage = `
mongosh /tmp/fixtures/migrations/migrate-rosalution-to-projects.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/migrations/migrate-rosalution-to-projects.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-rosalution-to-projects.js
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

const fs = require('fs')

db = db.getSiblingDB(databaseName);

const projectAbbreviationMapping = {
    "CILI":"Ciliopathies",
    "CPAM": "CPAM",
    "PAH": "PAH",
    "CCTS": "CCTS",
    "LW": "LW"
};

try {
    const usersByProjectPath = '/tmp/fixtures/migrations/users-by-projects.json'
    
    const fileContent = fs.readFileSync(usersByProjectPath, 'utf8');
    const usersJsonData = JSON.parse(fileContent);

    const projectsToInsert = Object.keys(usersJsonData)
        .map((projectName) => { return {name: projectName} })
        .map((projectFilter) => {
                return {
                    replaceOne: {
                        "filter": projectFilter,
                        "replacement": projectFilter,
                        "upsert": true
                    }
                }
            });

    db.projects.bulkWrite(projectsToInsert)

    const projectsObjectId = {};

    Object.keys(usersJsonData).forEach((projectName) => {
        if( !(projectName in projectsObjectId) ) {
            projectsObjectId[projectName] = db.projects.findOne({name: projectName});
        }
        
        usersJsonData[projectName].forEach((username) => {
            db.users.updateOne({"username": username}, {$addToSet: { project_ids: projectsObjectId[projectName]["_id"]}})
        });
    });

    const analyses = db.analyses.find();
    analyses.forEach(analysis => {
        
        Object.keys(projectAbbreviationMapping).some((abbreviation) => {
            const expression = RegExp(`^${abbreviation}`, 'g')

            if(analysis["name"].match(expression)) {
                const rosalutionProject = projectAbbreviationMapping[abbreviation];
                const projectDocument = projectsObjectId[rosalutionProject];

                db.analyses.updateOne({_id: analysis["_id"]}, {$set: {project_id: projectDocument["_id"]}});

                print(`Rosalution Project '${analysis['name']}' to project ${rosalutionProject}}`)

                return true
            }

            return false
        });
    });

} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
