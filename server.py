import socket
from _thread import *

myServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5555
IP = socket.gethostbyname(socket.gethostname())


try:
    myServer.bind((IP, port))
    print(f"[my server] Running on {socket.gethostname()} at {IP}:{port}")
except socket.error as e:
    print(str(e))

myServer.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:0,0", "1:100,100"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:

                arr = reply.split(":")
                print(f"Server Recieved player {arr[0]}'s position: \n" + reply)
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print(f"Sending the  player {nid}'s position to the client" + reply)
                if int(arr[1].split(",")[0]) >= 450:
                    print("The Winner is Player " + arr[0])

                    print("Connection Closed")
                    conn.close()
                    myServer.close()


            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
        conn, addr = myServer.accept()
        print("Connected to: ", addr)

        start_new_thread(threaded_client, (conn,))