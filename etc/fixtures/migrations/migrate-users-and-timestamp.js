const usage = `
mongosh /tmp/fixtures/migrations/migrate-users-and-timestamp.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/migrations/migrate-users-and-timestamp.js
    
    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-users-and-timestamp.js
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

usernameMapping = {
  'amoss01': '00bqd0d6r0dqpwptyuo8p6h3mnnumzee',
  'afoksin': 'h3bnr2uh1bo4oe0cs1rdyh3n5hrg71ej',
  'aeunoant': '00bqd0d6r0dqpwptyuo8p6h3mnnumzee',
}

usersToUpdate = Object.keys(usernameMapping);

db = db.getSiblingDB(databaseName)
try {
  const analyses = db.analyses.find();
  analyses.forEach(element => {

    element.timeline.forEach(event => {
      if(typeof(event.timestamp) === 'number') {
        // The timestamps from epoch were originally stored as seconds with
        // PyMongo not in milliseconds which is what the Mongosh Javascript
        // Shell is expecting
        event.timestamp = new Date(event.timestamp*1000)
        print(`Migrating case ${element.name}\t\tUpdating timeline event '${event.event}'\t\t${event.timestamp}...`)
      }

      if(usersToUpdate.includes(event.username)) {
        const oldUsername = event.username;
        event.username = usernameMapping[event.username]
        print(`Migrating case ${element.name}\t\tUpdating username to from '${oldUsername}' to clientId '${event.username}'...`)
      }
    });

    db.analyses.updateOne(
      {'_id': element._id},
      {'$set': element}
    );
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
