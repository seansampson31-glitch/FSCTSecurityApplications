import socket
import hashlib
import pyotp

# User database using SHA-256 hashes
# The 'sean' secret matches the client secret above for testing
users_db = {
    "sean": {
        "password_hash": hashlib.sha256("OldDog123".encode()).hexdigest(),
        "otp_secret": "JBSWY3DPEHPK3PXP",
        "failed_attempts": 0
        # b'\xb0\x96\x11S\x18\x8f+\x11\xd9\x1e\x0e\x87\x18r-\xb2\x8e\x9c\x01\x8c\x13\x17\xdfN\x95T\x81v\xae\x96\xcf\x91'
        # this would be my hash value for this, however, I cannot get this to work
    },
    "admin": {
        "password_hash": hashlib.sha256("Admin12345".encode()).hexdigest(),
        "otp_secret": pyotp.random_base32(),
        "failed_attempts": 0
    }
}

server_port = 12000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print("Security server is online and listening...")

    while True:
        conn, addr = server_socket.accept()
        print(f"New login attempt from: {addr}")
        
        try:
            authorized = False
            
            # --- PHASE 1: IDENTIFICATION ---
            conn.send("SEND_USER".encode())
            username = conn.recv(1024).decode().strip()
            
            if username not in users_db:
                conn.send("FAILURE: user not recognized".encode())
            
            elif users_db[username]["failed_attempts"] >= 3:
                conn.send("FAILURE: account locked due to too many attempts".encode())

            else:
                # --- PHASE 2: PASSWORD CHECK ---
                conn.send("SEND_PASS".encode())
                received_pwd = conn.recv(1024).decode().strip()
                hashed_input = hashlib.sha256(received_pwd.encode()).hexdigest()

                if hashed_input == users_db[username]["password_hash"]:
                    # --- PHASE 3: OTP CHECK ---
                    conn.send("SEND_OTP".encode())
                    received_otp = conn.recv(1024).decode().strip()
                    
                    totp = pyotp.TOTP(users_db[username]["otp_secret"])
                    
                    # Verify OTP (handles Part 5: clock drift via pyotp's verify)
                    if totp.verify(received_otp):
                        authorized = True
                        users_db[username]["failed_attempts"] = 0 
                        conn.send("SUCCESS".encode())
                    else:
                        users_db[username]["failed_attempts"] += 1
                        conn.send("FAILURE: invalid verification code".encode())
                else:
                    users_db[username]["failed_attempts"] += 1
                    conn.send("FAILURE: incorrect password".encode())

            # --- PHASE 4: SECURE SESSION ---
            while authorized:
                menu = f"\nUser: {username} | Commands: HELLO, MSG, EXIT\n"
                conn.sendall(menu.encode())
                
                data = conn.recv(1024).decode().strip()
                if not data or data.upper() == "EXIT":
                    authorized = False
                elif data.upper().startswith("HELLO"):
                    conn.sendall("Server says: Hello there!".encode())
                elif data.upper().startswith("MSG"):
                    conn.sendall(f"Server says: I got your message: {data[3:]}".encode())
        
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            conn.close()
            print("Client disconnected.")

finally:
    server_socket.close()
    
