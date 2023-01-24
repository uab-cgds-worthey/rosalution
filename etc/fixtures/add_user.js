// Declare the connection URI
const uri = 'mongodb://localhost:27017/rosalution_db';

// The default path to the fixtures, can be changed to a script argument in the future
const fixturePath = '/tmp/fixtures';

// Connect to the MongoDB instance using the connect function
const db = connect(uri);

const user_file = `${fixturePath}/`+process.argv[3];

console.log(`Connected to MongoDB with URI ${uri}`);
console.log(`Adding user from file ${user_file}`);

const fs = require('fs');
const users = JSON.parse(fs.readFileSync(user_file, 'utf8'));

try {
    let insertedUsers = []
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