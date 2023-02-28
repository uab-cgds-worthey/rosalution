const usage = `
mongosh /tmp/fixtures/add_user.js
    Script Options:
        help             if true print this help message
        userFile         default:  /tmp/fixtures/example-adding-users.json    file to read for new users
        databaseName     default:  rosalution_db    databaseName to use
    Run mongosh help for mongosh connection and authentication usage.
    Example: mongosh --host localhost --port 27017 --eval "var userFile='/tmp/fixtures/example.json'; databaseName='your_db_name'" /tmp/fixtures/add_user.js
    
    Run mongosh help for mongosh connection and authentication usage.
    `;

if (help === true) {
    print(usage);
    quit(1);
}

// Clean up input

// userFile
if (typeof userFile === 'undefined') {
    userFile = "/tmp/fixtures/example-adding-users.json";
} else if (typeof userFile !== 'string') {
    print("userFile must be a string");
    quit(1);
}

// databaseName
if (typeof databaseName === 'undefined') {
    databaseName = "rosalution_db";
} else if (typeof databaseName !== 'string') {
    print("databaseName must be a string");
    quit(1);
}

db = db.getSiblingDB(databaseName);

console.log(`Adding user from file ${userFile}`);



try {
    // Read the file
    const fs = require("fs");
    const users = JSON.parse(fs.readFileSync(userFile, "utf8"));
    var insertedUsers = [];
    users.forEach(user => {
        const existingUser = db.users.findOne({username: user.username});
        if (!existingUser) {
            db.users.insertOne(user);
            insertedUsers.push(user.username);
        } else {
            console.log(`Skipping user ${user.username} because it already exists`);
        }
    });
    console.log(`Inserted ${insertedUsers.length} users: ${insertedUsers}`);
} catch (err) {
    console.log(err.stack);
    console.log(usage);
    quit(1);
}
