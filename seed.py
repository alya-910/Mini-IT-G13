from app import create_app
from extensions import db
from models.items import Item
from models.message_model import ChatMessage
from models.user import User
import random

app = create_app()

with app.app_context():
    print("Dropping old database...")
    db.drop_all()
    print("Creating new database...")
    db.create_all()

    # --- 1. Create Users ---
    print("Creating users...")
    
    # Admin (You)
    admin = User(username="Admin123", email="admin@gmail.com", role="admin", status="active")
    admin.set_password("admin123")

    # Teammate 1: Siti Hawark
    user_siti = User(username="Siti123", email="sitihawark@gmail.com", role="user", status="active")
    user_siti.set_password("password123")

    # Teammate 2: Alya
    user_alya = User(username="Alya123", email="alya@gmail.com", role="user", status="active")
    user_alya.set_password("password123")

    db.session.add_all([admin, user_siti, user_alya])

    fake_users = [
        {"username": "AlexMarket", "email": "alex.m@example.com", "pw": "Pass123!_alex"},
        {"username": "john123", "email": "john.dev@test.com", "pw": "Siti_Secure99"},
        {"username": "TechGuru88", "email": "guru@webmail.org", "pw": "keyboard_warrior"},
        {"username": "UrbanExplorer", "email": "hello@explorer.com", "pw": "mountain_hike24"},
        {"username": "VintageVibes", "email": "shop@vintage.net", "pw": "retro_style77"},
        {"username": "ChefJordan", "email": "cooking@meals.com", "pw": "garlic_salt55"},
        {"username": "NightOwl", "email": "stayup@nocturnal.io", "pw": "moonlight_sonata"},
        {"username": "EcoFriendly", "email": "green@nature.com", "pw": "save_the_planet"}
    ]


    for data in fake_users:
        # 1. Create the user instance
        new_user = User(username=data['username'], email=data['email'])
        
        # 2. Use your existing method to hash the password
        new_user.set_password(data['pw'])
        
        # 3. Add to the session 'staging area'
        db.session.add(new_user)
    
    # 4. Commit everything at once (much faster!)
    db.session.commit()
    print(f"Done! Created {len(fake_users)} users.")

    db.session.commit()

    users = User.query.filter(User.username != 'Admin123').all()

    # --- 2. Create Listings ---
    print("Creating listings...")
    
    listing1 = Item(
        title="Sylvanian family figures",
        description="3 figures with all accessories included",
        price=30.0,
        status="active",
        seller_id=user_alya.id,
        image_path="uploads/sylvfam.jpeg"
    )

    listing2 = Item(
        title="Used Programming Textbook",
        description="Good condition, suitable for CS students.",
        price=30.0,
        status="active",
        seller_id=user_siti.id,
        image_path="uploads/programmingbook.jpg"
    )

    listing3 = Item(
        title="Uni Hoodie (Size M)",
        description="Slightly worn, still nice.",
        price=20.0,
        status="active",
        seller_id=user_siti.id,
        image_path="uploads/unisweater.jpg"
    )

    listing4 = Item(
        title="Scientific Calculator",
        description="Casio FX-570, includes cover.",
        price=15.0,
        status="active",
        seller_id=user_alya.id,
        image_path="uploads/calculator.jpg"
    )

    fake_listings = [
        {"title": "Cat stickers", "description": "100 unused stickers",  "price": 10, "image_path": "uploads/stickers.jpeg"},
        {"title": "Inspirational book", "description": "lightly used, good condition",  "price": 15, "image_path": "uploads/thinkingbook.jpeg"},
        {"title": "Wireless Headphones", "description": "Sony WH-CH710N, 2 years old, torn ear pad",  "price": 100, "image_path": "uploads/headphones.jpeg"},
        {"title": "Garmin watch", "description": "Vivoactive 5, no scratches, condition: 4/5",  "price": 600, "image_path": "uploads/watch.jpeg"},
        {"title": "Minimalist Desk Lamp", "description": "Ikea lamp with warm orange bulbs",  "price": 35, "image_path": "uploads/lamp.jpeg"},
        {"title": "Lego flower", "description": "Wildflower bouquet set(10313) , no box include",  "price": 75, "image_path": "uploads/legoflowers.jpeg"},
        {"title": "MMU tote bag", "description": "Barely used, like new",  "price": 7, "image_path": "uploads/mmutote.jpeg"},
        {"title": "White handbag", "description": "Pull & bear handbag with small pink stain",  "price": 35, "image_path": "uploads/handbag.jpeg"},
        {"title": "JBL speakers", "description": "Black jbl go 3",  "price": 65, "image_path": "uploads/speaker.jpeg"},
        {"title": "Demin jacket", "description": "Dusty grey levis jacket, size s (women)",  "price": 80, "image_path": "uploads/bluejacket.jpeg"},
        {"title": "Bluelight glasses", "description": "Coach blue light glasses",  "price": 200, "image_path": "uploads/bluelightglasses.jpeg"},
        {"title": "Ipad air M4", "description": "Purple ipad air M4 11', with pencil - 1700RM, with pencil - 1500RM",  "price": 1500, "image_path": "uploads/ipad.jpeg"},
        {"title": "Dictionaries", "description": "3 dictionaries to help with english courses",  "price": 30, "image_path": "uploads/dictionary.jpeg"}
    ]

    new_items = []

    for data in fake_listings:
            # Pick a random user from your 8 accounts
            random_owner = random.choice(users)
            item = Item(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                seller_id=random_owner.id,
                image_path=data['image_path']
            )
            new_items.append(item)

    db.session.add_all(new_items)
    db.session.add_all([listing1, listing2, listing3, listing4])
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