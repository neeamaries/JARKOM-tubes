import socket
import os
import time

HOST = "127.0.0.1"
PORT = 5001

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client_name = input("Masukkan Nama Client: ")

print(f"\nTerkoneksi dengan {(HOST, PORT)}")

while True:

    print("\n" + "=" * 40)
    print("MENU PENGIRIMAN")
    print("=" * 40)

    print("1. Kirim 1-5 Kata")
    print("2. Kirim 1 Kalimat Panjang")
    print("3. Kirim 1 Paragraf")
    print("4. Kirim TXT")
    print("5. Kirim DOCX")
    print("6. Kirim PDF")
    print("7. Kirim JPG")
    print("8. Kirim PNG")
    print("9. Kirim MP3")
    print("10. Kirim MP4")
    print("0. Keluar")

    pilihan = input("\nPilih menu: ")

    # =====================
    # KIRIM TEXT
    # =====================
    if pilihan in ["1", "2", "3"]:

        client.send("TEXT".encode())

        time.sleep(0.1)

        pesan = input("Masukkan pesan: ")
        pesan = f"[{client_name}] {pesan}"

        client.send(pesan.encode())

        print("Pesan berhasil dikirim")

    # =====================
    # KIRIM FILE
    # =====================
    elif pilihan in ["4", "5", "6", "7", "8", "9", "10"]:

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
            print(f"File tidak ditemukan: {path_file}")
            continue

        nama_file = os.path.basename(path_file)

        with open(path_file, "rb") as f:
            data = f.read()

        client.send("FILE".encode())

        time.sleep(0.1)

        header = f"{nama_file}|{len(data)}"

        client.send(header.encode())

        time.sleep(0.1)

        client.sendall(data)

        print(f"\n[{client_name}]")
        print(f"{nama_file} berhasil dikirim")

    elif pilihan == "0":
        break

    else:
        print("Menu tidak valid")

client.close()