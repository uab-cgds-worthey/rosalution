const usage = "\n\nmongosh --eval \"var help=false; [options]\" /tmp/fixtures/add_user.js\n" +
    "\nOptions:\n" +
    "    help             if true or undefined, print this help message\n" +
    "    userFile         default:  /tmp/fixtures/example-adding-users.json    file to read for new users\n" +
    "    host             default:  localhost    host to use in the URI for connecting to mongo\n" +
    "    port             default:  27017    port to use in the URI for connecting to mongo\n" +
    "    databaseName     default:  rosalution_db    databaseName to use\n" +
    "\nExample: mongosh --eval \"var help=false; userFile='/tmp/fixtures/example.json', host='127.0.0.1'," +
    " port='27017', databaseName='your_db_name'\" /tmp/fixtures/add_user.js\n";

if (typeof help === 'undefined' || help !== false) {
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

// Set the connection URI
var uri = "mongodb://" + host + ":" + port + "/" + databaseName;

// Connect to the MongoDB instance using the connect function
const db = connect(uri);

console.log(`Connected to MongoDB with URI ${uri}`);
console.log(`Adding user from file ${userFile}`);

const fs = require("fs");
const users = JSON.parse(fs.readFileSync(userFile, "utf8"));

try {
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
}