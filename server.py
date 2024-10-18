import socket
import threading

clients = []
client_names = {}
message_counts = {}
def broadcast(message, sender_name, sender_client):
    for client in clients:
        if client != sender_client:
            client.send(f"{sender_name}: {message}".encode('utf-8'))

def handle_client(client, server):
    name = client.recv(1024).decode('utf-8')
    client_names[client] = name
    print(f"{name} подключился.")
    clients.append(client)
    message_counts[client] = 0
    
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"{name}: {message}")
                broadcast(message, name, client)
                for other_client in clients:
                    if other_client == client:
                        message_counts[client] += 1
                    else:
                        message_counts[other_client] = 0
                if message_counts[client] >= 5:
                    client.send("Вы отправили 5 сообщений без ответа. Чат закрыт.".encode('utf-8'))
                    remove_client(client)
                    shutdown_server(server)
                    break
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def remove_client(client):
    if client in clients:
        # Получаем имя отключившегося клиента
        name = client_names[client]
        
        # Уведомляем остальных клиентов о том, что этот клиент отключился
        broadcast(f"{name} отключился.", "Сервер", client)
        
        print(f"{name} отключился.")  # Сообщение на стороне сервера
        
        # Удаляем клиента из списка
        clients.remove(client)
        client.close()
        
        # Удаляем данные о клиенте
        del client_names[client]
        del message_counts[client]

def shutdown_server(server):
    print("Сервер завершает работу...")
    for client in clients:
        client.close()
    server.close()
    exit(0)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(2)
    print("Сервер запущен. Ожидание подключения...")
    
    while True:
        try:
            client, address = server.accept()
            print(f"Подключен {address}")
            client.send("Введите ваше имя:".encode('utf-8'))
            thread = threading.Thread(target=handle_client, args=(client, server))
            thread.start()
        except:
            break

start_server()