from werkzeug.security import generate_password_hash, check_password_hash

users = {
    "admin": generate_password_hash("admin"),
    "doe": generate_password_hash("johndoe")
}