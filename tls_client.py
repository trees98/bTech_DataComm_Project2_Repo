from socket import *
import ssl

def connect_to_server(server_ip, server_port):
    try:
        #establish client socket
        client_socket = socket(AF_INET, SOCK_STREAM)
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations("server.crt")
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = False

        #wrap socket with TLS
        tls_socket = context.wrap_socket(client_socket, server_hostname=server_ip)
        tls_socket.connect((server_ip,server_port))
        print("You have connected to the server and traffic is encrypted")
        return tls_socket

    except:
        print("There was an issue establishing a connection:")
        return None

def send_and_receive(client_socket):
    #Handle sending messages and receiving responses.
    try:
        while True:
            message = input("Enter a number to check if it's even or odd (or 'exit' to quit): ")

            if message.lower() == "exit":
                client_socket.send(message.encode())
                print("Disconnecting... \nYou have disconnected")
                break

            client_socket.send(message.encode())
            response = client_socket.recv(2048).decode()
            print("From Server:", response)
    except:
        print("Please enter an int.")
#Specify the server IP and port number and call functions
def main():
    server_name = '127.0.0.1' #Change to server IP
    server_port = 15000

    client_socket = connect_to_server(server_name, server_port)
    if client_socket:
        try:
            send_and_receive(client_socket)
        finally:
            client_socket.close()

main()


