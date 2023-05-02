# server.py
import socket
import threading

# 创建一个服务器套接字，并开始监听连接
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.11.3', 8000))
server_socket.listen(100)

def handle_client(client_socket):
    while True:
        # 接收客户端消息并转发给其他客户端
        try:
            message = client_socket.recv(1024).decode('utf-8')
        except Exception:
            continue
        for other_socket in client_sockets:
            if other_socket != client_socket:
                try:
                    other_socket.send(message.encode('utf-8'))
                except Exception:
                    continue
                print("send")


# 客户端套接字列表
client_sockets = []

while True:
    # 接受新客户端连接，并为其创建一个新线程
    client_socket, address = server_socket.accept()
    client_sockets.append(client_socket)

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.daemon = True
    client_thread.start()
