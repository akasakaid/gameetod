# GameeTod

Program Auto klaim untuk wat token

# Daftar Isi
- [GameeTod](#gameetod)
- [Daftar Isi](#daftar-isi)
- [Dukung Hasil Pekerjaan Saya !](#dukung-hasil-pekerjaan-saya-)
- [Fitur](#fitur)
- [Cara Penggunaan](#cara-penggunaan)
  - [Tentang Proxy](#tentang-proxy)
  - [Tentang Config.json](#tentang-configjson)
  - [Windows](#windows)
  - [Linux](#linux)
  - [Termux](#termux)
- [Cara Mendapatkan Query](#cara-mendapatkan-query)
- [Kode Javascript untuk Mendapatkan Data di Aplikasi Telegram Desktop](#kode-javascript-untuk-mendapatkan-data-di-aplikasi-telegram-desktop)
- [Menjalankan Selama 24/7](#menjalankan-selama-247)
- [Diskusi](#diskusi)

# Dukung Hasil Pekerjaan Saya !

Jika anda suka dengan hasil pekerjaan saya anda bisa mendukung saya melakui tautan dibawah

- [Indonesia] https://s.id/nusanqr (QRIS)
- [Indonesia] https://trakteer.id/fawwazthoerif/tip
- [Global] https://sociabuzz.com/fawwazthoerif/tribe
- Jika anda ingin mengirim dalam bentuk lain, anda bisa menghubungi saya melalui telegram.

# Fitur

- [x] Klaim Otomatis Mining
- [x] Melakukan Spin Harian
- [x] Melakukan Spin Berbayar Menggunakan Ticket
- [x] Klaim Reward Event Mining Sebelumnya
- [ ] Melakukan Balapan (Race)

# Cara Penggunaan

## Tentang Proxy

Daftar di Website Berikut untuk Mendapatkan Proxy Gratis : [Here](https://www.webshare.io/?referral_code=dwj0m9cdi4mp)

Anda bisa menambahkan daftar proxy di file `proxies.txt` dan format proxynya seprti berikut :

Format :

```
http://host:port
http://user:pass@host:port
```

Contoh :

```
http://127.0.0.1:6969
http://user:pass@127.0.0.1:6969
socks5://127.0.0.1:6969
socks5://user:pass@127.0.0.1:6969
```

## Tentang Config.json

Ubah isi file `config.json` menggunakan aplikasi editor yang anda milikidan berikut adalah penjelasan tentang Nama (Key) dan Isi (Value) di dalam file config.json

| Nama (Key)             | Value (Isi)                | Deskripsi                                                                                   |
| ---------------------- | -------------------------- | ------------------------------------------------------------------------------------------- |
| countdown              | Angka Positif ( 1 - 99999) | Berfungsi untuk menetukan waktu jeda untuk klaim selanjutnya (satuan : detik)               |
| interval               | Angka Positif ( 1 - 99999) | Berfungsi untuk menetukan waktu jeda setiap akun (satuan : detik)                           |
| use_ticket_to_spin     | Boolean ( true / false)    | Berfungsi jika anda ingin melakukan spin menggunakan tiket, isi true untuk mengaktifkannya. |
| max_use_ticket_to_spin | Angka Positif ( 1- 9999)   | Berfungsi untuk menetukan maksimal tiket yang digunakan untuk spin                          |

## Windows 

1. Pastikan komputer anda telah terinstall python dan git.

    Saran: Gunakan python versi 3.8+ (3.8 keatas atau terbaru)
   
   python site : [https://python.org](https://python.org)
   
   git site : [https://git-scm.com/](https://git-scm.com/)

2. Clone / Duplikasi repository ini.
   ```shell
   git clone https://github.com/akasakaid/gameetod.git
   ```

3. Masuk ke folder gameetod
   ```
   cd gameetod
   ```

4. Install module / library yang dibutuhkan.
   ```
   python -m pip install -r requirements.txt
   ```

5. Edit / ubah file `data.txt`, masukkan data query ke dalam file `data.txt`. Anda bisa mendapatkan query anda dengan cara [Cara Mendapatkan Query](#cara-mendapatkan-query). Satu baris untuk 1 akun, jika anda ingin menambah akun ke-2 maka isi di baris yang baru.

6. Jalankan program / scriptnya.
   ```
   python bot.py
   ```

## Linux 

1. Pastikan komputer anda telah terinstall python dan git.

    Saran: Gunakan python versi 3.8+ (3.8 keatas atau terbaru)
   
   python
   ```shell
   sudo apt install python3 python3-pip
   ```
   git
   ```shell
   sudo apt install git
   ```

2. Clone / Duplikasi repository ini.
   ```shell
   git clone https://github.com/akasakaid/gameetod.git
   ```

3. Masuk ke folder gameetod
   ```
   cd gameetod
   ```

4. Install module / library yang dibutuhkan.
   ```
   python -m pip install -r requirements.txt
   ```

5. Edit / ubah file `data.txt`, masukkan data query ke dalam file `data.txt`. Anda bisa mendapatkan query anda dengan cara [Cara Mendapatkan Query](#cara-mendapatkan-query). Satu baris untuk 1 akun, jika anda ingin menambah akun ke-2 maka isi di baris yang baru.

6. Jalankan program / scriptnya.
   ```
   python bot.py
   ```

## Termux

1. Pastikan komputer anda telah terinstall python dan git.

    Saran: Gunakan python versi 3.8+ (3.8 keatas atau terbaru)
   
   python
   ```shell
   pkg install python
   ```
   git
   ```shell
   pkg install git
   ```

2. Clone / Duplikasi repository ini.
   ```shell
   git clone https://github.com/akasakaid/gameetod.git
   ```

3. Masuk ke folder gameetod
   ```
   cd gameetod
   ```

4. Install module / library yang dibutuhkan.
   ```
   python -m pip install -r requirements.txt
   ```

5. Edit / ubah file `data.txt`, masukkan data query ke dalam file `data.txt`. Anda bisa mendapatkan query anda dengan cara [Cara Mendapatkan Query](#cara-mendapatkan-query). Satu baris untuk 1 akun, jika anda ingin menambah akun ke-2 maka isi di baris yang baru.

6. Jalankan program / scriptnya.
   ```
   python bot.py
   ```


# Cara Mendapatkan Query

Data yang dibutuhkan sama seperti [pixelversebot](https://github.com/akasakaid/pixelversebot) jadi anda bisa menonton video panduan yang sama !

Berikut : [https://youtu.be/KTZW9A75guI](https://youtu.be/KTZW9A75guI)

# Kode Javascript untuk Mendapatkan Data di Aplikasi Telegram Desktop

```javascript
copy(Telegram.WebApp.initData)
```

# Menjalankan Selama 24/7

Anda bisa menjalankan script bot dalam 24/7 menggunakan vps / rdp. Anda bisa menggunakan aplikasi `screen` jika menggunakan sistem operasi linux untuk menjalakan script botnya di latar belakang.

# Diskusi

Jika anda memiliki pertanyaan atau yang lain, anda bisa bertanya disini : [@sdsproject_chat](https://t.me/sdsproject_chat)

