"""
Collection that handles the file attachments.
"""


class FileAttachmentCollection:
    "Collection that handles the file attachments."

    def __init__(self, bucket):
        """Initializes with the 'PyMongo' Collection object for the Analyses collection"""
        self.bucket = bucket

    def save_file(self, filestuff):
      # put returns the new  _id: ObjectId()
        self.bucket.put(filestuff)
