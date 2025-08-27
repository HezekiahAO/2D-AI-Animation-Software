from app import app  # Import data from my app code

with app.app_context():
    db.create_all():
    