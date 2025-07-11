from app.db.base import Base, engine
from app.db.models import customer, product, category  # Import all models to ensure they are registered

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done.")

if __name__ == "__main__":
    init_db()
