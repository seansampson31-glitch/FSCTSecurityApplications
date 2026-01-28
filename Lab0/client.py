import socket             

s = socket.socket()         

port = 12345                

s.connect(('127.0.0.1', port)) 
s.send("thanks for letting me connect".encode())

s.close()
