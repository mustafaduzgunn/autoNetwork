# passTools/passManager.py
import json
import os
import base64
from getpass import getpass
from cryptography.fernet import Fernet
from hashlib import sha256

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials.dat")

def derive_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(sha256(password.encode()).digest())

def encrypt_data(data: dict, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(json.dumps(data).encode())

def decrypt_data(data: bytes, key: bytes) -> dict:
    fernet = Fernet(key)
    return json.loads(fernet.decrypt(data).decode())

def load_or_create_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        print("credentials.dat dosyası bulunamadı.")
        password = getpass("Yeni bir ana parola oluşturun: ")
        key = derive_key(password)
        save_credentials({}, key)
        print("Yeni boş credential dosyası oluşturuldu.")
        return {}, key
    else:
        password = getpass("Ana parola: ")
        key = derive_key(password)
        try:
            with open(CREDENTIALS_FILE, "rb") as f:
                encrypted_data = f.read()
            credentials = decrypt_data(encrypted_data, key)
            return credentials, key
        except Exception:
            print("Parola yanlış ya da dosya bozulmuş.")
            exit(1)

def save_credentials(credentials: dict, key: bytes):
    encrypted_data = encrypt_data(credentials, key)
    with open(CREDENTIALS_FILE, "wb") as f:
        f.write(encrypted_data)

def user_menu(credentials: dict, key: bytes):
    while True:
        print("\n--- Kullanıcı Bilgileri ---")
        print("1 - Kullanıcı Ekle")
        print("2 - Kullanıcı Sil")
        print("3 - Kullanıcı Güncelle")
        print("4 - Kullanıcıları Listele")
        print("0 - Ana Menüye Dön")

        choice = input("Seçiminiz: ")

        if choice == "1":
            cred_id = input("Yeni kullanıcı ID'si: ")
            if cred_id in credentials:
                print("Bu ID zaten var.")
                continue
            username = input("Kullanıcı adı: ")
            password = getpass("Şifre: ")
            credentials[cred_id] = {"username": username, "password": password}
            save_credentials(credentials, key)
            print("Kullanıcı eklendi.")

        elif choice == "2":
            cred_id = input("Silinecek kullanıcı ID'si: ")
            if cred_id not in credentials:
                print("Bu ID bulunamadı.")
                continue
            del credentials[cred_id]
            save_credentials(credentials, key)
            print("Kullanıcı silindi.")

        elif choice == "3":
            cred_id = input("Güncellenecek kullanıcı ID'si: ")
            if cred_id not in credentials:
                print("Bu ID bulunamadı.")
                continue
            username = input("Yeni kullanıcı adı: ")
            password = getpass("Yeni şifre: ")
            credentials[cred_id] = {"username": username, "password": password}
            save_credentials(credentials, key)
            print("Kullanıcı güncellendi.")

        elif choice == "4":
            print("Kayıtlı kullanıcılar:")
            for cred_id in credentials:
                print(f"- {cred_id}")

        elif choice == "0":
            break

        else:
            print("Geçersiz seçim.")
