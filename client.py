import socket
import threading

# Функция для получения сообщений от сервера
def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("Ошибка соединения.")
            break

# Функция для отправки сообщений
def send_messages(client):
    while True:
        message = input()
        client.send(message.encode('utf-8'))

# Подключение к серверу
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))
    
    # Ввод имени
    name = input("Введите ваше имя: ")
    client.send(name.encode('utf-8'))

    # Запуск потоков для отправки и получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    send_thread = threading.Thread(target=send_messages, args=(client,))
    
    receive_thread.start()
    send_thread.start()

start_client()