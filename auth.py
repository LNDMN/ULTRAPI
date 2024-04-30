import json
from jose import jwt, JWTError
import bcrypt
from pony.orm import Database, Required, db_session, select

# Настройка базы данных
db = Database()
db.bind(provider='sqlite', filename='users.db', create_db=True)

class User(db.Entity):
    username = Required(str, unique=True)
    hashed_password = Required(str)
    roles = Required(str)  # Сериализуем роли в JSON или строку


db.generate_mapping(create_tables=True)

SECRET_KEY = "FS<k:OLXMY(ERY#&RMM{)!@YUMEX*!@YE(("
ALGORITHM = "HS256"


def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


from datetime import datetime, timedelta


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Токен действителен 15 минут
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@db_session
def create_user(username: str, password: str, roles: list):
    if select(u for u in User if u.username == username).exists():
        raise ValueError("User already exists")
    hashed_password = hash_password(password)
    User(username=username, hashed_password=hashed_password, roles=json.dumps(roles))
    return {"username": username, "roles": roles}


@db_session
def authenticate_user(username: str, password: str):
    user = User.get(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@db_session
def get_user(username: str):
    user = User.get(username=username)
    return user.to_dict() if user else None


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or get_user(username) is None:
            raise credentials_exception
        return {"username": username}
    except JWTError:
        raise credentials_exception
