#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
  Esse arquivo faz a capturação
  de banners ativos em portas TCP
  em endereços IP 

  Modificado em 08 de outubro de 2016
  por Vitor Mazuco (vitor.mazuco@gmail.com)
"""

import socket
import select
import sys


if len(sys.argv) != 4:
    print "Use - ./banner_grab.py [Endereço-IP] [Primeira Porta] [Ultima porta]"
    print "Exemplo - ./banner_grab.py 10.0.0.5 1 100"
    print "Esse exemplo irá pegar o banners para aporta TCP ports 1 ao 100 em 10.0.0.5"
    sys.exit()
    
ip = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])

for port in range(start,end):
    try:
        bangrab = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bangrab.connect((ip, port))
        ready = select.select([bangrab],[],[],1)
        if ready[0]:
            print "TCP Port " + str(port) + " - " + bangrab.recv(4096)
            bangrab.close()
    except:
        pass
