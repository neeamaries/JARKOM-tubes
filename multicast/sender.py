import socket
import os
import time

MCAST_GRP = "224.1.1.1"
PORT = 5002

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sender_name = input("Nama Sender: ")

sender_ip = socket.gethostbyname(
    socket.gethostname()
)

print("\n=== INFORMASI SENDER ===")
print(f"Nama Sender : {sender_name}")
print(f"IP Sender   : {sender_ip}")
print(f"Multicast   : {MCAST_GRP}")
print(f"Port        : {PORT}")

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

# PAKSA PAKAI WIFI INI
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_MULTICAST_IF,
    socket.inet_aton(sender_ip)
)

# LOOPBACK BIAR SENDER JUGA BISA NERIMA
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_MULTICAST_LOOP,
    1
)

while True:

    print("\n========================================")
    print("MULTICAST SENDER")
    print("========================================")

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

    elif pilihan == "0":
        break