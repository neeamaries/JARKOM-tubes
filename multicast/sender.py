import socket
import os
import time

MCAST_GRP = "224.1.1.1"
PORT = 5002

# Letak direktori
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sender_name = input("Nama Sender: ")

# Ambil IP WiFi aktif
temp = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

temp.connect(("8.8.8.8", 80))

sender_ip = temp.getsockname()[0]

temp.close()

print("\n=== INFORMASI SENDER ===")
print(f"Nama Sender : {sender_name}")
print(f"IP Sender   : {sender_ip}")
print(f"Multicast   : {MCAST_GRP}")
print(f"Port        : {PORT}")

# Alamat IPv4
sock = socket.socket(
    socket.AF_INET, 
    socket.SOCK_DGRAM,
    socket.IPPROTO_UDP
)

# TTL
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_MULTICAST_TTL,
    2
)

# PAKSA PAKAI WIFI
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_MULTICAST_IF,
    socket.inet_aton(sender_ip)
)

# LOOPBACK UNTUK SENDER
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_MULTICAST_LOOP,
    1
)

while True:
    print("\n")
    print(f"="*30)
    print("MULTICAST SENDER")
    print(f"="*30)

    print("1. Kirim 1-5 Kata")
    print("2. Kirim Kalimat Panjang")
    print("3. Kirim Paragraf")
    print("4. Kirim TXT")
    print("5. Kirim DOCX")
    print("6. Kirim PDF")
    print("7. Kirim JPG")
    print("8. Kirim PNG")
    print("9. Kirim MP3")
    print("10. Kirim MP4")
    print("0. Keluar")

    pilihan = input("Pilih: ")

    # PENGIRIMAN TEKS
    if pilihan in ["1", "2", "3"]:

        pesan = input("Masukkan pesan: ")

        paket = (
            f"TEXT|{sender_name}|"
            f"{sender_ip}|{pesan}"
        ).encode()

        sock.sendto(
            paket,
            (MCAST_GRP, PORT)
        )

        print("Pesan multicast terkirim")


    # PENGIRIMAN FILE
    elif pilihan in [
        "4", "5", "6",
        "7", "8", "9", "10"
    ]:

        file_map = {
            "4": os.path.join(BASE_DIR, "testing", "testTXT.txt"),
            "5": os.path.join(BASE_DIR, "testing", "testDocx.docx"),
            "6": os.path.join(BASE_DIR, "testing", "testPDF.pdf"),
            "7": os.path.join(BASE_DIR, "testing", "testJPG.jpg"),
            "8": os.path.join(BASE_DIR, "testing", "testPNG.png"),
            "9": os.path.join(BASE_DIR, "testing", "testMP3.mp3"),
            "10": os.path.join(BASE_DIR, "testing", "testMP4.mp4")
        }

        path_file = file_map[pilihan]

        if not os.path.exists(path_file):
            print("File tidak ditemukan")
            continue

        nama_file = os.path.basename(path_file)
        ukuran_file = os.path.getsize(path_file)

        sock.sendto(
            (
                f"FILE_START|"
                f"{sender_name}|"
                f"{sender_ip}|"
                f"{nama_file}|"
                f"{ukuran_file}"
            ).encode(),
            (MCAST_GRP, PORT)
        )

        time.sleep(0.3)

        with open(path_file, "rb") as f:

            while True:

                chunk = f.read(4096)

                if not chunk:
                    break

                sock.sendto(
                    chunk,
                    (MCAST_GRP, PORT)
                )

                time.sleep(0.001)

        time.sleep(0.3)

        sock.sendto(
            b"FILE_END",
            (MCAST_GRP, PORT)
        )

        print(f"{nama_file} berhasil dikirim")

    elif pilihan == "0":
        break
