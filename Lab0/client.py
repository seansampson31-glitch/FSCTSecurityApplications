import socket

client_socket = socket.socket()
port = 12345

client_socket.connect(('127.0.0.1', port))

# Need more parameters for usernames as ":" shouldn't be a valid username
my_name = input("Enter your username: ")
client_socket.send(("HELLO|" + my_name).encode())

welcome_msg = client_socket.recv(1024).decode()
print("Server Response: " + welcome_msg)

while True:
    print("\nOptions: Type a message then press enter to send, type quit then press enter to leave.")
    user_choice = input("Your message: ")

    if user_choice == "quit":
        client_socket.send("EXIT:".encode())
        bye_msg = client_socket.recv(1024).decode()
        print("Server says: " + bye_msg)
        break

    else:
        client_socket.send(("MSG:" + user_choice).encode())
        status = client_socket.recv(1024).decode()
        print("Server status: " + status)

client_socket.close()
