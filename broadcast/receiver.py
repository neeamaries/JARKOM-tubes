import socket
import os

PORT = 5003

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RECEIVED_DIR = os.path.join(
    BASE_DIR,
    "received_files"
)

os.makedirs(RECEIVED_DIR, exist_ok=True)

nama_receiver = input("Nama Receiver: ")

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

sock.bind(("", PORT))

print(f"\n{nama_receiver} menunggu broadcast...")

current_file = None
file_handle = None

sender_file = None
sender_ip_file = None

while True:

    data, addr = sock.recvfrom(65535)

    # =====================
    # TEXT
    # =====================
    if data.startswith(b"TEXT|"):

        pesan = data.decode(errors="ignore")

        parts = pesan.split("|", 3)

        sender = parts[1]
        sender_ip = parts[2]
        isi_pesan = parts[3]

        print("\n=== PESAN DITERIMA ===")
        print(f"Receiver : {nama_receiver}")
        print(f"Sender   : {sender}")
        print(f"IP       : {sender_ip}")
        print(f"Pesan    : {isi_pesan}")

    # =====================
    # FILE START
    # =====================
    elif data.startswith(b"FILE_START|"):

        parts = data.decode(
            errors="ignore"
        ).split("|")

        sender_file = parts[1]
        sender_ip_file = parts[2]
        nama_file = parts[3]

        path_file = os.path.join(
            RECEIVED_DIR,
            nama_file
        )

        file_handle = open(
            path_file,
            "wb"
        )

        current_file = nama_file

        print("\n=== MENERIMA FILE ===")
        print(f"Receiver : {nama_receiver}")
        print(f"Sender   : {sender_file}")
        print(f"IP       : {sender_ip_file}")
        print(f"Nama File: {nama_file}")

    # =====================
    # FILE END
    # =====================
    elif data == b"FILE_END":

        if file_handle:
            file_handle.close()

        print("\n=== FILE DITERIMA ===")
        print(f"Receiver : {nama_receiver}")
        print(f"Sender   : {sender_file}")
        print(f"IP       : {sender_ip_file}")
        print(f"Nama File: {current_file}")

        current_file = None
        sender_file = None
        sender_ip_file = None
        file_handle = None

    # =====================
    # FILE CHUNK
    # =====================
    else:

        if file_handle:
            file_handle.write(data)