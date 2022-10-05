"""
Collection that handels the GridFS bucket for the database.
"""

from bson import ObjectId

class GridFSBucketCollection:
    "Collection that handels the GridFS bucket for the database."

    def __init__(self, bucket):
        """Initializes with the 'PyMongo' Collection object for the Analyses collection"""
        self.bucket = bucket

    def check_if_exists(self, filename):
        """Returns true if the file exists in the database"""
        return self.bucket.exists(filename=filename)

    def save_file(self, file, filename):
        """Saves the file to the database using the GridFS bucket and returns the file id"""
        return self.bucket.put(file, filename=filename)

    def list_files(self):
        """Returns a list of all the files in the database"""
        return self.bucket.list()

    def get_file(self, file_id):
        """Returns the file with the given id"""
        if isinstance(file_id, str):
            file_id = ObjectId(file_id)
            print("File id: ", file_id)
            print(type(file_id))
        return self.bucket.get(file_id)

    def find_file_by_name(self, filename):
        """Returns the file with the given name"""
        return self.bucket.find_one({"filename": filename}).read()
