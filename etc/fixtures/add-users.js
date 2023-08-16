// docker exec -it rosalution-rosalution-db-1 mongosh /tmp/fixtures/add-cpam-users.js

const fs = require('fs');

// this file has been removed for security reasons
// To add users in the future create a csv file in the below path in the following format
// Name,blazerid,email,clientid,scope
// John Doe,jdoe,jdoe@site.com,<generated client id>,scope

const inputPath = `/tmp/fixtures/usersToImport.csv`
var newUsersList = [];

var csvData = fs.readFileSync(inputPath)
    .toString() // convert Buffer to string
    .split('\n') // split string to lines
    .map(e => e.trim()) // remove white spaces for each line
    .map(e => e.split(',').map(e => e.trim())); // split each line to array

console.log(csvData)

for(let i = 0; i < csvData.length; i++) {
    if(csvData[i][0] == 'Name')
        continue;

    user = {
      username: '',
      full_name: '',
      email: '',
      scope: '',
      hashed_password: '$2b$12$xmKVVuGh6e0wP1fKellxMuOZ8HwVoogJ6W/SZpCbk0EEOA8xAsXYm',
      disabled: 'false',
      client_id: '',
      client_secret: ''
    }

    user.username = csvData[i][1]
    user.full_name = csvData[i][0]
    user.email = csvData[i][2]
    user.scope = csvData[i][4]
    user.client_id = csvData[i][3]

    newUsersList.push(user);
}

db = db.getSiblingDB('rosalution_db');

try {
    let usersToAdd = []
    for(newUser in newUsersList) {      
      const dbUser = db.users.findOne({'username': newUsersList[newUser].username})

      if (dbUser == null) {
        usersToAdd.push(newUsersList[newUser])
      }
    }

    // console.log("THESE ARE THE NEW USERS TO ADD!!")

    if(usersToAdd.length == 0) {
      console.log("No new users to add, they all exist already.")
    }
    else {
      usersToAdd.forEach(user => {db.users.insertOne(user)});
      console.log(`CPAM users updated!`);
    }
    
} catch (err) {
    console.log(err.stack);
    console.log(usage);
    quit(1);
}
