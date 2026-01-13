class Config:
    SECRET_KEY = "dev-secret-key"  # change if you want
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
