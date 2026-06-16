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

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
    socket.IPPROTO_UDP
)

sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_MULTICAST_TTL,
    2
)

while True:

    print("\n" + "=" * 40)
    print("MULTICAST SENDER")
    print("=" * 40)

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

    # =====================
    # TEXT
    # =====================
    if pilihan in ["1", "2", "3"]:

        pesan = input("Masukkan pesan: ")

        paket = f"TEXT|{pesan}".encode()

        sock.sendto(
            paket,
            (MCAST_GRP, PORT)
        )

        print("Pesan multicast terkirim")

    # =====================
    # FILE
    # =====================
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

        sock.sendto(
            f"FILE_START|{nama_file}".encode(),
            (MCAST_GRP, PORT)
        )

        time.sleep(0.2)

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

        time.sleep(0.2)

        sock.sendto(
            b"FILE_END",
            (MCAST_GRP, PORT)
        )

        print(
            f"{nama_file} berhasil dikirim"
        )

    elif pilihan == "0":
        break