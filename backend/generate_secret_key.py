import secrets

def generate_secret_key():
    """Generate a secure Django secret key"""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))

if __name__ == '__main__':
    print("Generated SECRET_KEY:")
    print(generate_secret_key())
    print("\nAdd this to your .env file:")
    print(f"SECRET_KEY={generate_secret_key()}")
