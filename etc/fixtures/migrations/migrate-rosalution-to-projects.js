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

try {
    const usersByProjectPath = '/tmp/fixtures/migrations/users-by-projects.json'
    
    const fileContent = fs.readFileSync(usersByProjectPath, 'utf8');
    const usersJsonData = JSON.parse(fileContent);

    
    db.createCollection("projects");

    const projectsToInsert = Object.keys(usersJsonData).map((projectName) => {
        return {name: projectName} });
    db.projects.insertMany(projectsToInsert);
    Object.keys(usersJsonData).forEach((projectName) => {
        const projectDocument = db.projects.findOne({name: projectName})
        usersJsonData[projectName].forEach((username) => {
            db.users.updateOne({"username": username}, {$addToSet: { projects: projectDocument["_id"]}})
        })
    })
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
