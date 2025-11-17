🔗 Airdrop-Style File Transfer (Python)
A simple and lightweight Airdrop-like file transfer system built using Python sockets. This project allows you to send and receive files over a local network with real-time progress tracking.

 Features
*  Send files over LAN
*  Receive files automatically
*  Progress bar using tqdm
*  Fast and lightweight
*  Works on Windows, Mac, and Linux
*  Supports all file types


Project Structure

├── sender.py     # Script to send files
└── server.py     # Script to receive files

Installation
1. Install Python 3
2. Install required dependency:

pip install tqdm

Usage
1. Start the Receiver (Server)
Run:  python3 server.py
You will see:
[*] Listening as 0.0.0.0:5001

2. Send a File
Run: python3 sender.py
Enter:
* File path
* Receiver’s IP address
Transfer begins with a progress bar.

Stopping the Server
Press: CTRL + C
to stop listening for connections.

Troubleshooting
* Ensure both devices are on the same Wi-Fi network
* Allow Python through firewall if connection fails
* Use correct local IP of the receiver (e.g., 192.168.x.x)
