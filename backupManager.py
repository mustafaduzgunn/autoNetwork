# backupManager.py
import os
import json
from datetime import datetime
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

def load_inventory():
    with open("data/inventory.json") as f:
        return json.load(f)

def load_commands():
    with open("data/commands.json") as f:
        return json.load(f)

def perform_backup(devices, credentials, commands_dict):
    if not os.path.exists("backups"):
        os.makedirs("backups")

    for device in devices:
        name = device["name"]
        ip = device["ip"]
        device_type = device["device_type"]
        cred_id = device["credential_id"]

        if cred_id not in credentials:
            print(f"[HATA] {name} ({ip}) - Kimlik bilgisi bulunamadı: {cred_id}")
            continue

        username = credentials[cred_id]["username"]
        password = credentials[cred_id]["password"]
        commands = commands_dict.get("backup", {}).get(device_type, [])

        if not commands:
            print(f"[HATA] {name} ({ip}) - Bu cihaz türü için komut bulunamadı: {device_type}")
            continue

        try:
            conn = ConnectHandler(
                device_type=device_type,
                host=ip,
                username=username,
                password=password
            )

            output = ""
            for cmd in commands:
                output += f"{cmd}\n{conn.send_command(cmd)}\n\n"

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"backups/{timestamp}_{name}_{ip}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(output)

            print(f"[OK] {name} ({ip}) - Backup alındı.")

            conn.disconnect()

        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            print(f"[HATA] {name} ({ip}) - {str(e)}")
        except Exception as e:
            print(f"[HATA] {name} ({ip}) - Beklenmeyen hata: {str(e)}")

def get_devices_by_tag(inventory, tag):
    return [device for device in inventory if tag in device.get("tags", [])]
