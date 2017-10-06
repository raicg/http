# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP
#

# importacao das bibliotecas
import socket
from datetime import datetime
import os.path

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor



def getHead(f, caminho):
    time = os.path.getctime(caminho)
    return """
Date: %s
Server: O meu servidor/v1 (Aula de Redes)
Content-Length: %s
Connection: %s
""" % (datetime.fromtimestamp(time), len(f.readlines()), caminho)




# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print 'Servidor HTTP aguardando conexoes na porta %s ...' % PORT

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    
    # declaracao da resposta do servidor
    comando = request.split(" ")[0]
    caminho = request.split(" ")[1]
    versao = request.split(" ")[2]
    if (comando == 'get'):

        if (os.path.isfile(caminho)):
            f=open(caminho , 'r')
            texto = "HTTP/1.1 200 OK \r\n\r\n%s\r\n" %f.read()
            f.close()

        else:
            f=open('404.html','r')
            texto = "HTTP/1.1 404 Not Found \r\n\r\n%s\r\n" %f.read()
            f.close()



    elif (comando == 'head'):

        if (os.path.isfile(caminho)):
            f=open(caminho , 'r')
            texto = getHead(f,caminho)
            f.close()

        else:
            f=open('404.html','r')
            texto = "HTTP/1.1 404 Not Found \r\n\r\n%s\r\n" %f.read()
            f.close()




    else:
         f=open('400.html','r')
         texto = "HTTP/1.1 400 Bad Request \r\n\r\n%s\r\n" %f.read()
         f.close()
    

    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(texto)
    # encerra a conexao
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()
