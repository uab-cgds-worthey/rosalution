/* Usage & arguments:
    * docker-compose exec -T rosalution-db mongosh /tmp/fixtures/add_user.js /tmp/fixtures/example-adding-users.json
    * docker-compose exec -T rosalution-db mongosh /tmp/fixtures/add_user.js <user-file-path> <host> <port> <database_name>
    *
    * Non-option arguments:
    * user-file-path: path to the user file
    *
    * These Arguments are optional, defaults are:
    * <host> = localhost
    * <port> = 27017
    * <database_name> = rosalution
    *
    * Example:
    * docker-compose exec -T rosalution-db mongosh /tmp/fixtures/add_user.js /tmp/fixtures/example-adding-users.json localhost 27017 rosalution_db
*/


// Declare the variables for the URI connection
var host = "localhost";
var port = "27017";
var database_name = "rosalution_db";

// Check for the presence of each argument, and update its value if it's present
for (let i = 4; i < process.argv.length; i++) {
    if (process.argv[i] === "--script-host" || process.argv[i] === "-sh") {
        host = process.argv[i + 1];
    } else if (process.argv[i] === "--script-port" || process.argv[i] === "-sp") {
        port = process.argv[i + 1];
    } else if (process.argv[i] === "--script-database" || process.argv[i] === "-sd") {
        database_name = process.argv[i + 1];
    }
}

// Set the connection URI
var uri = "mongodb://" + host + ":" + port + "/" + database_name;

// Connect to the MongoDB instance using the connect function
const db = connect(uri);

const user_file = process.argv[3];

console.log(`Connected to MongoDB with URI ${uri}`);
console.log(`Adding user from file ${user_file}`);

const fs = require("fs");
const users = JSON.parse(fs.readFileSync(user_file, "utf8"));

try {
    var insertedUsers = [];
    users.forEach(user => {
        const existingUser = db.users.findOne({username: user.username});
        if (!existingUser) {
            db.users.insertOne(user);
            insertedUsers.push(user.username);
        } else {
            console.log(`User ${user.username} already exists.`);
        }
    });
    console.log(`Inserted ${insertedUsers.length} users: ${insertedUsers}`);
} catch (err) {
    console.log(err.stack);
}