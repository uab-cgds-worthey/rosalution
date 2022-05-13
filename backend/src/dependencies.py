from .annotation import AnnotationQueue
from .database import Database

from cas import CASClient

print("logging statement")

# Database/Repositories
fake_mongodb_client = {}
database = Database(fake_mongodb_client)

# Queue that processess annotation tasks safely between threads
annotation_queue = AnnotationQueue()

# URLs for interacting with UAB CAS Padlock system for BlazerID
cas_client = CASClient(
    version=3,
    service_url='http://dev.cgds.uab.edu/divergen/api/login?nexturl=%2Fdivergen',
    server_url='https://padlockdev.idm.uab.edu/cas/'
)