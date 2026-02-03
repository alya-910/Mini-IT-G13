class Config:
    SECRET_KEY = "cart-secret-key"  # change if you want  # Needed for session (cart)
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # uploads
    UPLOAD_FOLDER = 'static/profile_pics'

    # email system
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '36df090f947a3e'
    MAIL_PASSWORD = '50704eb8222b6e'
    MAIL_DEFAULT_SENDER = 'no-reply@thriftwize.com'
