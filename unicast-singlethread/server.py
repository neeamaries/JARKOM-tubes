import socket
import os

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server berjalan di port {PORT}")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RECEIVED_DIR = os.path.join(BASE_DIR, "received_files")

os.makedirs(RECEIVED_DIR, exist_ok=True)

while True:

    conn, addr = server.accept()

    print(f"\nTerkoneksi dengan {addr}")

    try:

        while True:

            jenis = conn.recv(1024).decode()

            if not jenis:
                break

            # =====================
            # TERIMA TEXT
            # =====================
            if jenis == "TEXT":

                pesan = conn.recv(4096).decode()

                print("\n=== PESAN DITERIMA ===")
                print(pesan)

            # =====================
            # TERIMA FILE
            # =====================
            elif jenis == "FILE":

                header = conn.recv(1024).decode()

                if "|" not in header:
                    print("Header file tidak valid")
                    continue

                nama_file, ukuran = header.split("|")

                ukuran = int(ukuran)

                path_simpan = os.path.join(
                RECEIVED_DIR,
                nama_file
                )

                with open(path_simpan, "wb") as f:

                    total = 0

                    while total < ukuran:

                        chunk = conn.recv(
                            min(4096, ukuran - total)
                        )

                        if not chunk:
                            break

                        f.write(chunk)
                        total += len(chunk)

                print("\n=== FILE DITERIMA ===")
                print(f"Nama File : {nama_file}")
                print(f"Ukuran    : {ukuran} bytes")
                print(f"Lokasi    : {path_simpan}")

    except Exception as e:

        print("Error:", e)

    finally:

        conn.close()
        print("Client terputus")