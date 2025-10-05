import bcrypt

def hash_password_direct(password: str) -> str:
    """Hash password using bcrypt directly"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password_direct(password: str, hashed: str) -> bool:
    """Verify password using bcrypt directly"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

password = "t3st!"
print(f"Password: '{password}'")
print(f"Password length: {len(password)} characters")
print(f"Password bytes: {len(password.encode('utf-8'))} bytes")
print(f"Password bytes repr: {password.encode('utf-8')}")

try:
    hashed = hash_password_direct(password)
    print(f"Hash successful: {hashed[:50]}...")

    # Test verification
    is_valid = verify_password_direct(password, hashed)
    print(f"Verification successful: {is_valid}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")