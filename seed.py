from app import create_app
from extensions import db
from models import User, Listing, Message, Report

app = create_app()

with app.app_context():
    print("Dropping old database...")
    db.drop_all()
    print("Creating new database...")
    db.create_all()

    # --- 1. Create Users ---
    print("Creating users...")
    
    # Admin (You)
    admin = User(name="Admin", email="admin@gmail.com", role="admin", status="active")
    admin.set_password("admin123")

    # Teammate 1: Siti Hawark
    user_siti = User(name="Siti Hawark", email="sitihawark@gmail.com", role="user", status="active")
    user_siti.set_password("password123")

    # Teammate 2: Alya
    user_alya = User(name="Alya", email="alya@gmail.com", role="user", status="active")
    user_alya.set_password("password123")

    db.session.add_all([admin, user_siti, user_alya])
    db.session.commit()

    # --- 2. Create Listings ---
    print("Creating listings...")
    
    listing1 = Listing(
        title="Used Programming Textbook",
        description="Good condition, suitable for CS students.",
        price=30.0,
        status="active",
        user_id=admin.id,
    )

    listing2 = Listing(
        title="Uni Hoodie (Size M)",
        description="Slightly worn, still nice.",
        price=20.0,
        status="active",
        user_id=user_siti.id,
    )

    listing3 = Listing(
        title="Scientific Calculator",
        description="Casio FX-570, includes cover.",
        price=15.0,
        status="active",
        user_id=user_alya.id,
    )

    db.session.add_all([listing1, listing2, listing3])
    db.session.commit()

    # --- 3. Create Messages ---
    print("Creating messages...")
    msg1 = Message(
        content="Hi Siti, is the hoodie still available?",
        sender_id=user_alya.id,
        receiver_id=user_siti.id,
    )
    
    msg2 = Message(
        content="Yes Alya, it's still available!",
        sender_id=user_siti.id,
        receiver_id=user_alya.id,
    )

    db.session.add_all([msg1, msg2])
    db.session.commit()

    print("✅ Database created with Admin, Siti Hawark, and Alya.")