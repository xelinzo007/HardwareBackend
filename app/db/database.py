from app.db.base import SessionLocal

# FastAPI-compatible DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
