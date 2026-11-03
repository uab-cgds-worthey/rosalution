const usage = `
mongosh /tmp/fixtures/migrations/migrate-discussion-content-to-arrays.js
    Script Options:
        help: if true print this help message
    
    Run mongosh help for mongosh connection and authentication usage.
    
    Example: 
    
    mongosh --host localhost --port 27017 --eval "var help=true;" /tmp/fixtures/migrations/migrate-discussion-content-to-arrays.js
    
    // docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-discussion-content-to-arrays.js
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
    print(`Migrating case ${element.name} -----`)

    // Change discussion and reply content to arrays instead of strings
    element.discussions.forEach(post=> {
      if ('string' == typeof(post.content)) {
        convertedString = String(post.content)
        post.content = convertedString.split('\n')
      }

      post.thread.forEach(reply=> {
        if ('string' == typeof(reply.content)) {
          convertedString = String(reply.content)
          reply.content = convertedString.split('\n')
        }
      });
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