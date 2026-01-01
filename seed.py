from app import create_app          # CHANGE 1: Import the function
from extensions import db
from models import User, Listing, Message

# CHANGE 2: Create the app instance manually
app = create_app()

with app.app_context():
    print("Dropping old database...")
    db.drop_all()
    print("Creating new database...")
    db.create_all()

    # Users
    print("Creating users...")
    admin = User(name="Admin", email="admin@gmail.com", role="admin", status="active")
    admin.set_password("admin123")

    user1 = User(name="Kelly", email="kelly@gmail.com", role="user", status="active")
    user1.set_password("user123")

    db.session.add_all([admin, user1])
    db.session.commit()

    # Listings
    print("Creating listings...")
    listing1 = Listing(
        title="Used Programming Textbook",
        description="Good condition, suitable for CS students.",
        price=30.0,
        user_id=admin.id,
    )
    listing2 = Listing(
        title="Uni Hoodie (Size M)",
        description="Slightly worn, still nice.",
        price=20.0,
        user_id=user1.id,
    )

    # Messages
    print("Creating messages...")
    msg1 = Message(
        content="Hi, is the hoodie still available?",
        sender_id=admin.id,
        receiver_id=user1.id,
    )
    msg2 = Message(
        content="Yes, it's still available!",
        sender_id=user1.id,
        receiver_id=admin.id,
    )

    db.session.add_all([listing1, listing2, msg1, msg2])
    db.session.commit()

    print("✅ Database created with sample users, listings and messages.")
