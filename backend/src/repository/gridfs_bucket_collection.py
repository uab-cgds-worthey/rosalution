"""
Collection that handles the GridFS bucket for the database.
"""

from bson import ObjectId


class GridFSBucketCollection:
    "Collection that handles the GridFS bucket for the database."

    def __init__(self, bucket):
        """Initializes with the 'PyMongo' Collection object for the Analyses collection"""
        self.bucket = bucket

    def filename_exists(self, filename):
        """Returns true if the file with filename exists in the database"""
        return self.bucket.exists(filename=filename)

    def id_exists(self, file_id):
        """Returns true if the file with file_id exists in the database"""
        for char in file_id:
            if char not in "0123456789abcdef":
                return False
        if isinstance(file_id, str):
            file_id = ObjectId(file_id)
        return self.bucket.exists(file_id)

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

    def get_analysis_file_by_id(self, file_id):
        """Returns the file with the given name"""
        grid_out = self.bucket.find_one({"_id": ObjectId(str(file_id))})

        while True:
            chunk = grid_out.readchunk()
            if not chunk:
                break
            yield chunk

    def delete_file(self, file_id):
        """Deletes the file with the given id"""
        # Warning: Any processes/threads reading from the file while this method is executing will likely see an
        # invalid/corrupt file. Care should be taken to avoid concurrent reads to a file while it is being deleted.
        #
        # Note: Deletes of non-existent files are considered successful since the end result is the same: no file with
        # that _id remains.
        # see https://pymongo.readthedocs.io/en/stable/api/gridfs/index.html
        if isinstance(file_id, str):
            file_id = ObjectId(file_id)
        return self.bucket.delete(file_id)
