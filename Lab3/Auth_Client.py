import socket
import pyotp
import getpass

def run_test_client():
    server_ip = '127.0.0.1'
    server_port = 12000
    
    # We use a fixed secret so it matches our test user 'sean' on the server
    # In a real app, this would be scanned via QR code or saved locally
    otp_secret = "JBSWY3DPEHPK3PXP"
    totp = pyotp.TOTP(otp_secret)
    # Base secret

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try: 
        client_socket.connect((server_ip, server_port))

        while True:
            response = client_socket.recv(1024).decode()

            if response == "SEND_USER":
                username = input("Enter your username: ")
                client_socket.sendall(username.encode())
            
            elif response == "SEND_PASS":
                # getpass hides the typing for a more professional feel
                password = getpass.getpass("Enter your password: ")
                client_socket.sendall(password.encode())

            elif response == "SEND_OTP":
                # Part 2: Generate current code
                current_code = totp.now()
                print(f"-- [Local Sync] Current OTP is: {current_code} --")
                otp_input = input("Enter the 6-digit verification code: ")
                client_socket.sendall(otp_input.encode())

            elif response == "SUCCESS":
                print("\nLogin successful! Welcome to the secure area.")
                # Post-auth command loop
                while True:
                    server_msg = client_socket.recv(1024).decode()
                    print(server_msg)
                    cmd = input("Command > ")
                    client_socket.sendall(cmd.encode())
                    if cmd.upper() == "EXIT":
                        print("Closing connection...")
                        return

            elif "FAILURE" in response:
                print(f"Access Denied: {response}")
                break
    
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_test_client()
