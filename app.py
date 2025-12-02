from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db

def create_app():
    app = Flask(__name__)

    
    # configure SQL Alchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)
    
    # import blueprints
    from routes.auth import auth
    from routes.main import main

    # register bluepints
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app

app = create_app()
        

if __name__ == '__main__':
    
    app.run(debug=True)

