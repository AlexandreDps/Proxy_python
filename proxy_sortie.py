# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 18:19:56 2023

@author: Alexandre
"""
import socket,rsa
from generate_keys import read_RSA_keys
from threading import Thread

public_key,private_key = read_RSA_keys()


class Proxy_Sortie():
    
    def __init__(self,host,port,buffer_size):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        
    def start(self):
        proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        proxy.bind((self.host, self.port))
        proxy.listen() 
        print("\n [+] Exit proxy started successfully")
        
        while True :
            print(" [-] Waiting for the encrypted request")
            entry_proxy,adress = proxy.accept()
            print(f" [+] Connexion with {adress} established")
            
            client_thread = Thread(target=self.handle_client, args=(entry_proxy,adress))
            client_thread.start()
        
        
    def handle_client(self, entry_proxy,adress):
        request = entry_proxy.recv(self.buffer_size)
        print(f'req : {request}')
        #Déchiffrage de la requête :
        request = rsa.decrypt(request, private_key)
        
        print(f" [+] Decrypted request : {request} ")
        target_HOST = request.decode('UTF-8').split("\n")[1].split(" ")[1].strip()
        
        exit_proxy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        exit_proxy_client.connect((target_HOST, 80))
        exit_proxy_client.sendall(request)
        response = exit_proxy_client.recv(4096)
        
        chunk_size = 1024 #Because RSA 8192 can only encrypt 1024bytes of data
        chunks = [response[i:i+chunk_size] for i in range(0, len(response), chunk_size)]
        #On chiffre la réponse
        for chunk in chunks:
            encrypted_chunk = rsa.encrypt(chunk, public_key)
            entry_proxy.send(encrypted_chunk)
            
        print(' [+] Crypted chunks successfully sent')
        entry_proxy.close()
        print(f" [-] Connexion with {adress} closed")


#Démarage du proxy de sortie avec les paramètres spécifiés
exit_HOST = 'localhost'
exit_PORT = 9999
buffer_size = 4096
proxy_server = Proxy_Sortie(exit_HOST, exit_PORT, buffer_size)
proxy_server.start()