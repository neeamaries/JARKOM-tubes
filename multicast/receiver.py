import socket
import struct

MCAST_GRP = "224.1.1.1"
PORT = 5002

nama_receiver = input("Nama Receiver: ")

receiver_ip = socket.gethostbyname(
    socket.gethostname()
)

print("\n=== INFORMASI RECEIVER ===")
print(f"Nama Receiver : {nama_receiver}")
print(f"IP Receiver   : {receiver_ip}")
print(f"Multicast     : {MCAST_GRP}")
print(f"Port          : {PORT}")

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
    socket.IPPROTO_UDP
)

sock.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

sock.bind(("", PORT))

mreq = struct.pack(
    "4s4s",
    socket.inet_aton(MCAST_GRP),
    socket.inet_aton(receiver_ip)
)

sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq
)

print(f"\n{nama_receiver} menunggu multicast...")

while True:

    data, addr = sock.recvfrom(65535)

    pesan = data.decode(
        errors="ignore"
    )

    print("\n=== PESAN DITERIMA ===")
    print(f"Receiver : {nama_receiver}")
    print(f"Dari     : {addr}")
    print(pesan)