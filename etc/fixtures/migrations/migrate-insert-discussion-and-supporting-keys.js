const usage = `
mongosh /tmp/fixtures/migrations/migrate-insert-discussion-and-supporting-keys.js

    Script Options:
        help : Bool : Optional
            - If True print this help message
        databaseName : String : Optional
            - Default: rosalution_db

    Run mongosh help for mongosh connection and authentication usage.

    Example:

    mongosh --host localhost --port 27017 --eval 'var help=True;' /tmp/fixtures/migrations/migrate-insert-discussion-and-supporting-keys.js

    docker exec -it <rosalution_db_container> mongosh /tmp/fixtures/migrations/migrate-insert-discussion-and-supporting-keys.js
`

if (help === true) {
    print(usage);
    quit(1);
}

if (typeof databaseName === 'undefined') {
    databaseName = 'rosalution_db';
} else if (typeof databaseName !== 'string') {
    print('databaseName must be a string');
    print(usage);
    quit(1);
}

db = db.getSiblingDB(databaseName)

function keyCheck(analyses) {
    for(analysis in analyses) {
        // console.log(analyses[analysis])
        const analysisName = analyses[analysis]['name']
        const discussionsKeyExist = "discussions" in analyses[analysis]
        const supportingKeyExist = "attachments" in analyses[analysis]
        console.log(`${analysisName}: 
          'supporting' - ${supportingKeyExist}, 'discussions' - ${discussionsKeyExist}`);
    }
}

try {
    let analyses = db.analyses.find({}).toArray();
    
    console.log("=== Before ===")
    keyCheck(analyses)

    for(i in analyses) {
        if(!("attachments" in analyses[i]))
            analyses[i]['attachments'] = []
        if(!("discussions" in analyses[i]))
            analyses[i]['discussions'] = []

        db.analyses.updateOne({'_id': analyses[i]._id}, {'$set': analyses[i]})
    }

    console.log("=== After ===")
    keyCheck(analyses)
} catch(e) {
    console.log(e.stack);
    console.log(usage);
    quit(1);
}
