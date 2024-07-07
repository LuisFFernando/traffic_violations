import os

JWT_SECRET = os.getenv("JWT_SECRET", "my_app_test")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
