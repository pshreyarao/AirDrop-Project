# server.py
import socket
import tqdm
import os

# Device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Create the server socket
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    # Receive file info
    received = client_socket.recv(BUFFER_SIZE).decode()
    
    # Handle empty or broken connections
    if not received:
        print("[!] Empty request received, skipping.")
        client_socket.close()
        continue

    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    # Receive file
    print(f"[+] Receiving file: {filename}")
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        bytes_read_total = 0
        while bytes_read_total < filesize:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            bytes_read_total += len(bytes_read)
            progress.update(len(bytes_read))

    print(f"[+] File {filename} received successfully.\n")
    client_socket.close()
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
