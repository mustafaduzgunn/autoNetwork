# autoNetwork
Network Automation Tools For Cisco, Huawei, H3C, Dell, Arista, Ruijie vs.


# Ağ Cihazları Yedekleme ve Yönetim Aracı

Bu Python uygulaması, ağ cihazlarının konfigürasyonlarını otomatik olarak yedeklemek için geliştirilmiştir. Cisco, Huawei, H3C gibi farklı cihaz türlerini destekler. Kullanıcı bilgileri şifreli olarak saklanır, cihazlar tag’lere göre gruplanabilir.

---

## 🚀 Özellikler

- Ana parola ile güvenli giriş
- Şifreli kullanıcı bilgileri yönetimi
- Cihazlara bağlanarak konfigürasyon yedeği alma (Netmiko ile)
- Cihazlara `tag`’lere göre gruplama
- Komutları `commands.json` dosyasından çekme
- Yedekleri zaman damgalı dosya adıyla `backups/` klasörüne kaydetme
- Hatalı bağlantılarda uyarı mesajı

---

## 📁 Klasör Yapısı

autoNetwork/
├── main.py
├── backupManager.py
├── requirements.txt
├── .gitignore
├── README.md
├── backups/
├── data/
│ ├── inventory.json
│ └── commands.json
└── passTools/
├── passManager.py
└── credentials.dat


python -m venv venv

Windows:
venv\Scripts\activate

MacOS / Linux
source venv/bin/activate

pip install -r requirements.txt
