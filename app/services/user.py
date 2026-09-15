from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import RegisterUserRequest, LoginUserRequest
from app.utils.security import hash_password, verify_password
from app.exceptions import DuplicateUserError, InvalidCredentialsError

def register_user(
        db: Session,
        request: RegisterUserRequest
        ) -> User:
    existing_user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_user is not None:
        raise DuplicateUserError(
            "A user with this email already exists."
        )

    hashed_password = hash_password(request.password)

    new_user = User(
        username=request.username,
        email=request.email,
        password_hash=hashed_password
        )

    db.add(new_user)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(new_user)

    return new_user

def login_user(
        db: Session,
        login_request: LoginUserRequest
    ) -> User:

    user = (
        db.query(User)
        .filter(User.email == login_request.email)
        .first()
    )

    if user is None:
        raise InvalidCredentialsError(
            "Invalid email or password."
        )

    if not verify_password(
        login_request.password, 
        user.password_hash
        ):
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

    return user