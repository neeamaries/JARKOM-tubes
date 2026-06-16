import socket
import threading
import os

HOST = "0.0.0.0"
PORT = 5001

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECEIVED_DIR = os.path.join(BASE_DIR, "received_files")

os.makedirs(RECEIVED_DIR, exist_ok=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server Multithread Aktif di port {PORT}")

client_counter = 0


def handle_client(conn, addr, client_id):

    print(f"\nClient {client_id} terhubung")

    try:

        while True:

            jenis = conn.recv(1024).decode(errors="ignore")

            if not jenis:
                break

            # =====================
            # TEXT
            # =====================
            if jenis == "TEXT":

                pesan = conn.recv(4096).decode(errors="ignore")

                print("\n=== PESAN DITERIMA ===")
                print(f"Client ID : {client_id}")
                print(pesan)

            # =====================
            # FILE
            # =====================
            elif jenis == "FILE":

                header = conn.recv(1024).decode(errors="ignore")

                if "|" not in header:
                    print(f"Client {client_id}: Header tidak valid")
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
                print(f"Client ID : {client_id}")
                print(f"Nama File : {nama_file}")
                print(f"Ukuran    : {ukuran} bytes")
                print(f"Lokasi    : {path_simpan}")

    except Exception as e:

        print(f"\nClient {client_id} Error:")
        print(e)

    finally:

        conn.close()
        print(f"Client {client_id} terputus")


while True:

    conn, addr = server.accept()

    client_counter += 1

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr, client_counter)
    )

    thread.start()