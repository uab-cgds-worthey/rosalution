"""
Collection that handles the file attachments.
"""


class FileAttachmentCollection:
    "Collection that handles the file attachments."

    def __init__(self, bucket):
        """Initializes with the 'PyMongo' Collection object for the Analyses collection"""
        self.bucket = bucket

    def save_file(self, filestuff):
        """Saves the file to the database using the GridFS bucket and returns the file id"""
      # put returns the new  _id: ObjectId()
        self.bucket.put(filestuff)

    def get_file(self, file_id):
        """Returns the file with the given id"""
        return self.bucket.get(file_id)

    def list_files(self):
        """Returns a list of all the files in the database"""
        return self.bucket.list()
