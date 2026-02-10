import socket

server_socket = socket.socket()
port = 12345
server_socket.bind(('', port))
server_socket.listen(5)

print("Server is running and waiting...")

while True:
    connection, address = server_socket.accept()
    print("New person joined from:", address)

    logged_in = False
    name = ""
    # starting my username

    while True:
        message = connection.recv(1024).decode()

        if not message:
            break

        if "|" not in message:
            connection.send("ERROR|Missing symbol".encode())
            continue

        parts = message.split("|")
        command = parts[0]
        content = parts[1]

        if command == "HELLO":
            name = content
            logged_in = True
            print(name + " signed in.")
            connection.send(("OK|Hello " + name).encode())

        elif logged_in == False:
            connection.send("ERROR|HELLO false".encode())

        elif command == "MSG":
            print(name + " says: " + content)
            connection.send("OK|Message sent".encode())

        elif command == "EXIT":
            print(name + " is quitting.")
            connection.send("OK|Goodbye".encode())
            break
        
        else:
            connection.send("ERROR|Command not found".encode())

    connection.close()
    print("Connection finished.")
    