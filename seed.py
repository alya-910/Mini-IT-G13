from app import create_app
from extensions import db
from models.listing import Listing
from models.message_model import ChatMessage
from models.user import User

app = create_app()

with app.app_context():
    print("Dropping old database...")
    db.drop_all()
    print("Creating new database...")
    db.create_all()

    # --- 1. Create Users ---
    print("Creating users...")
    
    # Admin (You)
    admin = User(username="Admin123", name="Admin", email="admin@gmail.com", role="admin", status="active")
    admin.set_password("admin123")

    # Teammate 1: Siti Hawark
    user_siti = User(username="Siti123", name="Siti Hawark", email="sitihawark@gmail.com", role="user", status="active")
    user_siti.set_password("password123")

    # Teammate 2: Alya
    user_alya = User(username="Alya123", name="Alya", email="alyahanisa@gmail.com", role="user", status="active")
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
    msg1 = ChatMessage(
        body="Hi Siti, is the hoodie still available?",
        sender_id=user_alya.id,
        receiver_id=user_siti.id,
    )
    
    msg2 = ChatMessage(
        body="Yes Alya, it's still available!",
        sender_id=user_siti.id,
        receiver_id=user_alya.id,
    )

    db.session.add_all([msg1, msg2])
    db.session.commit()

    print("✅ Database created with Admin, Siti Hawark, and Alya.")