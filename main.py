import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(folder, script):
    path = os.path.join(BASE_DIR, folder, script)

    if os.path.exists(path):
        subprocess.run(["python", path])
    else:
        print(f"File tidak ditemukan: {path}")

while True:

    print("\n" + "=" * 50)
    print("TUGAS BESAR JARINGAN KOMPUTER")
    print("=" * 50)

    print("1. Unicast Single Thread - Server")
    print("2. Unicast Single Thread - Client")

    print("3. Unicast Multi Thread - Server")
    print("4. Unicast Multi Thread - Client")

    print("5. Multicast - Sender")
    print("6. Multicast - Receiver")

    print("7. Broadcast - Sender")
    print("8. Broadcast - Receiver")

    print("0. Keluar")

    pilihan = input("\nPilih menu: ")

    if pilihan == "1":
        run_script("unicast-singlethread", "server.py")

    elif pilihan == "2":
        run_script("unicast-singlethread", "client.py")

    elif pilihan == "3": 
        run_script("unicast-multithread", "server.py")  

    elif pilihan == "4":
        run_script("unicast-multithread", "client.py")

    elif pilihan == "5":
        run_script("multicast", "sender.py")

    elif pilihan == "6":
        run_script("multicast", "receiver.py")

    elif pilihan == "7":
        run_script("broadcast", "sender.py")

    elif pilihan == "8":
        run_script("broadcast", "receiver.py")

    elif pilihan == "0":
        print("Program selesai.")
        break

    else:
        print("Pilihan tidak valid.")