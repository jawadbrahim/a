import os

class Development:
 DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:jawadibrahim10@localhost:5432/projects")
