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
var host = "";
var port = "";
var database_name = "";

// if the arguments are not passed, use the default values
if (process.argv.length < 5) {
    host = "localhost";
    port = "27017";
    database_name = "rosalution_db";
} else {
    host = process.argv[4];
    port = process.argv[5];
    database_name = process.argv[6];
}
// set the connection URI
var uri = "mongodb://" + host + ":" + port + "/" + database_name;

// Connect to the MongoDB instance using the connect function
const db = connect(uri);

const user_file = process.argv[3];

console.log(`Connected to MongoDB with URI ${uri}`);
console.log(`Adding user from file ${user_file}`);

const fs = require("fs");
const users = JSON.parse(fs.readFileSync(user_file, "utf8"));

try {
    var insertedUsers = []
    users.forEach(user => {
        const existingUser = db.users.findOne({username: user.username});
        if (!existingUser) {
            db.users.insertOne(user);
            insertedUsers.push(user.username)
        } else {
            console.log(`User ${user.username} already exists.`);
        }
    });
    console.log(`Inserted ${insertedUsers.length} users: ${insertedUsers}`);
} catch (err) {
    console.log(err.stack);
}