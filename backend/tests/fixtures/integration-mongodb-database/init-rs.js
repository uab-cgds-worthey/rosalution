// Check if the replica set is already initialized; if not, initialize it.
try {
  var status = rs.status();
  print("Replica set already initialized with status: " + status.ok);
} catch (e) {
  print("Initializing replica set...");
  
  var config = {
    _id: "rs0",
    members: [
      { _id: 0, host: "localhost:27017" }
    ]
  };
  
  var res = rs.initiate(config);
  print("Initialization result: " + JSON.stringify(res));
}