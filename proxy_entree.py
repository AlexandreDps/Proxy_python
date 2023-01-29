# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 18:19:43 2023

@author: Alexandre
"""
from threading import Thread
import rsa,socket
from generate_keys import generate_RSA_keys,read_RSA_keys
import time
#Uncomment line below to generate new private and public keys in .pem files
#generate_RSA_keys(8192) 
public_key,private_key = read_RSA_keys()

class Proxy():
    
    def __init__(self,host,port,buffer_size,exit_host,exit_port):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.exit_host = exit_host
        self.exit_port = exit_port
        
    def start(self):
        proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        proxy.bind((self.host, self.port))
        proxy.listen() 
        print("\n [+] Proxy started successfully")
        
        while True :
            print(" [-] Waiting for http request")
            client_socket,adress = proxy.accept()
            print(f" [+] Connexion with {adress} established")
            
            #Start a new Thread
            client_thread = Thread(target=self.handle_client, args=(client_socket,adress))
            client_thread.start()

    def handle_client(self,client_socket,adress):
        request = client_socket.recv(self.buffer_size)
        print(f" [+] req : {request}")
        #Chiffrement de la requête avec RSA
        request = rsa.encrypt(request, public_key)
        
        proxy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_client.connect((self.exit_host, self.exit_port))
        print(" [+] Proxy_client successfully linked with Exit_proxy")
        proxy_client.sendall(request)
        
        
        #Getting responses from server
        #Responses are chunked because they are cypted in RSI(8192) and are usually bigger than 1024bytes
        response = []
        while True :
            encrypted_data = proxy_client.recv(self.buffer_size)
            try: response.append(encrypted_data)
            except : break
            if not encrypted_data:
                break
        fresponse = b''
        for i in response :
            try :fresponse += rsa.decrypt(i, private_key)
            except: break
        
        client_socket.sendall(fresponse)
        proxy_client.close()
        print(f" [-] Connexion with {adress} closed")


#Démarage du proxy client avec les paramètres spécifiés
host = 'localhost'
port = 9998
exit_HOST = 'localhost'
exit_PORT = 9999
buffer_size = 4096
proxy_client = Proxy(host,port,buffer_size,exit_HOST,exit_PORT)
proxy_client.start()
