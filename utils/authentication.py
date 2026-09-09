import re
import bcrypt
from utils.database import user_by_email, create_user

def signup(name, email, password, confirm):
    if not all([name.strip(), email.strip(), password, confirm]): return False, "All fields are required."
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email): return False, "Enter a valid email address."
    if len(password) < 8: return False, "Password must contain at least 8 characters."
    if password != confirm: return False, "Passwords do not match."
    if user_by_email(email): return False, "An account already exists for this email."
    create_user(name.strip(), email, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
    return True, "Account created. Please sign in."

def login(email, password):
    user=user_by_email(email)
    if not user or not bcrypt.checkpw(password.encode(), user["password_hash"].encode()): return None
    return user
