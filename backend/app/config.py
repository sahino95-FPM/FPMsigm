import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://credef:credef@localhost:3306/credef")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/uploads")
