"""
Contains all the configuration variables used thoughout the application.
These parameters have the intention that they can be changed/modified at runtime to provide deployment configuration.
Specifically the SECRET_KEY parameter can be generated and changed with each run so it is not the same each time.
"""

SECRET_KEY = "ed6b87fcaf3be62fd13bcdcb2d5de7acccc30d35b1b01f8f6b8fe273c34df0bd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
TOKEN_URL = "/divergen/api/auth/token"
SECURITY_SCOPES = {
        "read": "View the pages on diverGen.",
        "write": "Add/Remove information from diverGen analyses.",
        "modify": "Add/Remove analyses themselves." }
