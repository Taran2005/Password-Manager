from cryptography.fernet import Fernet
from getpass import getpass
import os

KEY_FILE = 'key.key'
PASSWORD_FILE = 'passwords.txt'

def generate_key():
    return Fernet.generate_key()

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        return None

def save_key(key):
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def initialize_fernet(key):
    return Fernet(key)

def encrypt_password(password, f):
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, f):
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()

def add_password(fernet_instance):
    name = input("Enter the site name: ")
    url = input("Enter the site URL: ")
    username = input("Enter the Username: ")
    password = getpass("Enter the Password: ")

    with open(PASSWORD_FILE, 'a') as file_handle:
        encrypted_password = encrypt_password(password, fernet_instance)
        file_handle.write(f"Name: {name} | URL: {url} | Username: {username} | Password: {encrypted_password.decode()}\n")

def view_passwords(fernet_instance):
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file_handle:
            for line in file_handle.readlines():
                data = line.strip().split(" | ")
                name, url, username, encrypted_password = data
                decrypted_password = decrypt_password(encrypted_password.encode(), fernet_instance)
                print(f"Name: {name} | URL: {url} | Username: {username} | Password: {decrypted_password}")
    else:
        print("No passwords stored yet.")

def main():
    master_password = getpass("Enter your master password: ")
    key = load_key()
    if key is None:
        print("Generating new key...")
        key = generate_key()
        save_key(key)

    fernet_instance = initialize_fernet(key + master_password.encode())

    while True:
        print("\n1. Add a new Password")
        print("2. View existing Passwords")
        print("Enter q to quit")
        mode = input("\n")

        if mode == "q":
            print("Goodbye!")
            break
        elif mode == "1":
            add_password(fernet_instance)
        elif mode == "2":
            view_passwords(fernet_instance)
        else:
            print("Invalid mode")

if __name__ == "__main__":
    main()
