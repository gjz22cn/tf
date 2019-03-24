import socket
import os

BUFSIZE = 1024
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_port = ('127.0.0.1', 9999)
for root, dirs, files in os.walk('./data/pre_image/'):
    for file in files:
        msg = os.path.join(root, file)
        #msg = input(">> ").strip()
        client.sendto(msg.encode('utf-8'), ip_port)
        data, server_addr = client.recvfrom(BUFSIZE)
        print('客户端recvfrom ', data.decode(), server_addr)

client.close()
