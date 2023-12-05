import threading
import socket

host= '127.0.0.1'
port= 3389

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.1.113',port))
server.listen()

clients=[]
nicknames=[]

def brodcast(message):
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            message= client.recv(1024)
            brodcast(message)
        except:
            index= clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            brodcast(f'{nickname} left the chat!! '.encode('ascii'))
            break

def receive():
    while True:
        client, adress = server.accept()
        print(f"connected with {str(adress)}")
        client.send('NICK'.encode('ascii'))
        nickname= client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname of the client is {nickname}!!')
        brodcast(f'{nickname} joined the chat!!!'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))
        
        
        thread= threading.Thread(target=handle, args=(client,))
        thread.start()
        
print('Server is alive now....!')       
receive()

        
        
    
