from werkzeug.security import generate_password_hash, check_password_hash

users = {
    "admin": generate_password_hash("admin"),
    "doe": generate_password_hash("johndoe")
}

dummyPasswords = ['admin', 'admin123', 'district', 'district123', '1234']
dummyRentalTypes = ['Auto', 'House', 'Machinary', 'Wedding', 'Electricians']
dummyRentalPics = ['/auto', '/house', '/machinary', '/wedding', '/electricians']

'''{
	"fname": "John",
	"lname": "Doe",
	"email": "john.doe@example.com",
	"password_1": "admin123",
	"password_2": "admin123"
}'''