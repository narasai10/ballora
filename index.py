import socket
import pyautogui as pg
import base64
import time
import keyboard

def salvar_imagem(imagem_base64):
    try:
        with open("screenshot.png", "wb") as img_file:
            img_file.write(base64.b64decode(imagem_base64))
        print("📸 Screenshot recebido e salvo como screenshot.png!")
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 6783))  # Aqui você define o IP e porta
server_socket.listen(1)

print("Aguardando conexão...")
client_socket, addr = server_socket.accept()
print(f"Conexão estabelecida com {addr}")

while True:
    msg_resposta = input("Digite sua resposta: ")
    client_socket.send(msg_resposta.encode())
    if msg_resposta.lower() == "screenshot":
        imagem_base64 = client_socket.recv(100000000).decode()  # Recebe a string base64 da imagem
        salvar_imagem(imagem_base64)
    elif msg_resposta.lower() == "start-control mouse":
        print("🔄 Controle do mouse ativado!\nD - Clique")
        while True:
            if keyboard.is_pressed("f"):
                break
            # acao = input("\nComando para parar (stop-control mouse): ")

            # if acao.lower() == "stop":
            #     client_socket.sendall(acao.encode())
            #     print("❌ Controle do mouse desativado.")
            #     break  # Sai do modo controle do mouse
            
            mousex, mousey = pg.position()
            pressed_d = 1
            if keyboard.is_pressed("d"):
                pressed_d = 0
            client_socket.sendall(f"{str(mousex)},{str(mousey)},{str(pressed_d)}\n".encode())
            time.sleep(0.2)
    else:
        resposta = client_socket.recv(4096).decode()
        print(f"Resposta do cliente:\n{resposta}")

client_socket.close()
