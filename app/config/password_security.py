import bcrypt
import base64

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    # Encode the hashed password in Base64
    hashed_password_base64 = base64.b64encode(hashed_password).decode('utf-8')
    return hashed_password_base64

def check_password(password, hashed_password_base64):
    # Decode the Base64 encoded hashed password
    hashed_password = base64.b64decode(hashed_password_base64.encode('utf-8'))
    # Check if the password matches the hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)

if __name__ == "__main__":

    password = "Password1"
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")

    # Verify password
    is_correct = check_password("Test_Password0", hashed)
    print(f"Password is correct: {is_correct}")

