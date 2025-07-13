from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user import User, UserPermission
from app.schemas.user import UserCreate, UserOut
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check for duplicate email/username
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Save permissions
    for perm in user.permissions:
        db_perm = UserPermission(user_id=db_user.id, permission_name=perm)
        db.add(db_perm)
    db.commit()

    return UserOut(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        role=db_user.role,
        created_at=db_user.created_at,
        permissions=user.permissions
    )

@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    result = []
    for user in users:
        perms = [perm.permission_name for perm in user.permissions]
        result.append(UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            permissions=perms
        ))
    return result
