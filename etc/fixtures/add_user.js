const usage = `
mongosh /tmp/fixtures/add_user.js
    Options:
        help             if true print this help message
        userFile         default:  /tmp/fixtures/example-adding-users.json    file to read for new users
        host             default:  localhost    host to use in the URI for connecting to mongo
        port             default:  27017    port to use in the URI for connecting to mongo
        databaseName     default:  rosalution_db    databaseName to use
    Example: mongosh --eval "var userFile='/tmp/fixtures/example.json'; host='127.0.0.1', port='27017', databaseName='your_db_name'" /tmp/fixtures/add_user.js`;

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
// host
if (typeof host === 'undefined') {
    host = "localhost";
} else if (typeof host !== 'string') {
    print("host must be a string");
    quit(1);
}

// port
if (typeof port === 'undefined') {
    port = "27017";
} else if (typeof port !== 'string') {
    print("port must be a number");
    quit(1);
}

// databaseName
if (typeof databaseName === 'undefined') {
    databaseName = "rosalution_db";
} else if (typeof databaseName !== 'string') {
    print("databaseName must be a string");
    quit(1);
}

conn = new Mongo();
db = conn.getDB(databaseName);

db = db.getSiblingDB(databaseName);

// // Set the connection URI
// var uri = "mongodb://" + host + ":" + port + "/" + databaseName;

// // Connect to the MongoDB instance using the connect function
// const db = connect(uri);

console.log(`Connected to MongoDB with URI ${uri}`);
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