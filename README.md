---

Crypto Alert Bot

Bot Telegram untuk memantau harga kripto (Bybit) dan membuat alert otomatis.
Dibangun dengan Python, SQLite, dan python-telegram-bot v13.


---

🚀 Fitur

Perintah /price SYMBOL → tampilkan harga terbaru (BTCUSDT, ETHUSDT, dll)

Perintah /setalert SYMBOL above|below PRICE

Perintah /alerts → daftar alert milik pengguna

Perintah /remove ID → hapus alert

Worker background mengecek harga tiap interval dan mengirim alert saat kondisi terpenuhi

Penyimpanan alert di SQLite (alerts.db)

Bisa dijalankan di Termux atau VPS



---

🛠 Instalasi

1. Clone repository

git clone git@github.com:fazulfi/crypto-alert-bot.git
cd crypto-alert-bot

2. Buat virtualenv & install dependency

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


---

🔑 Konfigurasi Environment

Copy .env.example menjadi .env:

cp .env.example .env
nano .env

Isi variabel berikut:

TELEGRAM_TOKEN=xxxx:yyyyyyyyyyyyyyyy
CHECK_INTERVAL=5

CHECK_INTERVAL = interval detik untuk worker cek harga.

> ⚠️ Jangan commit .env ke GitHub.




---

🧪 Menjalankan Bot (Development Mode)

Gunakan ini untuk debugging:

source venv/bin/activate
python bot_alert.py

Jika berhasil, bot akan merespon perintah Telegram.


---

🔧 Menjalankan Bot di Background (Termux)

Agar bot tetap hidup meski Termux ditutup:

termux-wake-lock
tmux new -s bot
source venv/bin/activate
python bot_alert.py

Detach tmux (biarkan berjalan di background):

Ctrl + b, lalu d

Untuk melihat lagi:

tmux attach -t bot


---

📌 Perintah Telegram

Berikut daftar perintah pengguna:

1. Lihat harga

/price BTCUSDT

2. Set alert

/setalert BTCUSDT above 70000
/setalert ETHUSDT below 2500

3. Cek daftar alert

/alerts

4. Hapus alert

/remove 3


---

🗄 Struktur Database (SQLite)

Database otomatis dibuat saat bot pertama kali berjalan: alerts.db

Tabel:

kolom	tipe	deskripsi

id	integer	primary key
chat_id	text	chat Telegram pemilik alert
symbol	text	contoh: BTCUSDT
direction	text	above atau below
price	real	target harga
triggered	integer	0 atau 1
created_at	text	timestamp



---

🌐 Migrasi ke VPS

Di VPS cukup jalankan:

git pull
source venv/bin/activate
python bot_alert.py

Atau di tmux:

tmux new -s bot
source venv/bin/activate
python bot_alert.py


---

✔ Lisensi

Private use — bebas dipakai sendiri.


---
