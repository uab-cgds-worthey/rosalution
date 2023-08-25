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

db = db.getSiblingDB(databaseName);

try {
  const analyses = db.analyses.find();
  analyses.forEach(element => {

    // print(element.timeline)

    element.timeline.forEach(event => {
      if(typeof(event.timestamp) === 'number') {
        print(`Migrating case ${element.name} -----`)

        print(`TIMELINE Event: ${event.timestamp}`)
        event.timestamp = new Date(event.timestamp)
        print('Updating event')
        print(event)
        print('--------------------------')

      }

      // print(typeof event.timestamp)
    });
    // // Add Decision Section to Brief 
    // const briefSection = element.sections.find( section => section.header === 'Brief');

    // if( !briefSection.content.find(row => row.field === 'Decision') ) {
    //   briefSection.content.push({
    //     'type': 'section-text',
    //     'field': 'Decision',
    //     value: [],
    //   });
    // };

    // db.analyses.updateOne(
    //   {'_id': element._id},
    //   {'$set': element}
    // );
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
