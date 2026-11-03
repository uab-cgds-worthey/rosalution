if (help === true) {
  print(usage);
  quit(1);
}

if (typeof databaseName === 'undefined') {
  databaseName = 'rosalution_db';
} else if (typeof databaseName !== 'string') {
  print('databaseName must be a string');
  quit(1);
}

db = db.getSiblingDB(databaseName);

const scopeMappings = {
  'developer': 'write',
  'pre-clinical-intake': 'write',
  'researcher': 'read',
  'bioinformatics-section-user': 'write',
}

const oldScopes = Object.keys(scopeMappings)

try {
  const users = db.users.find();
  users.forEach(userElement => {

    if(oldScopes.includes(userElement.scope)) {
      print(`Migrating '${userElement.username}' from '${userElement.scope}' to '${scopeMappings[userElement.scope]}'...`)
      userElement.scope = scopeMappings[userElement.scope]
    }

    // update       
    db.users.updateOne(
      {'_id': userElement._id},
      {'$set': userElement}
    )
  });
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}

print("Migration Operation Complete For User Scopes")