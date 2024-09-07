def secure_password(password: str) :
    if len(password) < 8 or len(password) > 20:
        return False
    special_characters = set('" "!@#$%^&*()-+?_=,<>/""|;:')
    has_lower = has_upper = has_number = has_special = False

    for character in password:
        if character.islower():
            has_lower = True
        elif character.isupper():
            has_upper = True
        elif character.isdigit():
            has_number = True
        elif character in special_characters:
            has_special = True
        
        if has_lower and has_upper and has_number and has_special:
            return True

    return False

def test_secure_password_more_than_20_characters():
    # Arrange
    password = "abcdefghijklmnopqrstuvwxyz1234567890"
    
    # Act
    result = secure_password(password)
    
    # Assert
    assert result == True

test_secure_password_more_than_20_characters()