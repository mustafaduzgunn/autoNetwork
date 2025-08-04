# main.py
from passTools.passManager import load_or_create_credentials, user_menu
from backupManager import load_inventory, load_commands, perform_backup, get_devices_by_tag

def main_menu():
    credentials, key = load_or_create_credentials()

    while True:
        print("\n--- Ana Menü ---")
        print("1 - Kullanıcı Bilgileri")
        print("2 - Backup İşlemleri")
        print("0 - Çıkış")

        secim = input("Seçiminiz: ")

        if secim == "1":
            user_menu(credentials, key)

        elif secim == "2":
            backup_menu(credentials)

        elif secim == "0":
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçim.")

def backup_menu(credentials):
    inventory = load_inventory()
    commands = load_commands()

    while True:
        print("\n--- Backup Menüsü ---")
        print("1 - Full Backup")
        print("2 - Tag'e Göre Backup")
        print("0 - Ana Menüye Dön")

        secim = input("Seçiminiz: ")

        if secim == "1":
            perform_backup(inventory, credentials, commands)

        elif secim == "2":
            tag = input("Tag girin: ")
            filtered_devices = get_devices_by_tag(inventory, tag)
            if not filtered_devices:
                print("Bu tag'e ait cihaz bulunamadı.")
                continue
            perform_backup(filtered_devices, credentials, commands)

        elif secim == "0":
            break

        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main_menu()
