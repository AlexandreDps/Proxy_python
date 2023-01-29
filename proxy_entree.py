# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 18:19:43 2023

@author: Alexandre
"""

import rsa,socket,ast
from generate_keys import generate_RSA_keys,read_RSA_keys
import zlib

#Uncomment line below to generate new private and public keys in .pem files
#generate_RSA_keys(4096) 
public_key,private_key = read_RSA_keys()

HOST = 'localhost'
PORT = 9998
Exit_HOST = 'localhost'
Exit_PORT = 9999
BUFFER = 4096

entry_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
entry_proxy.bind((HOST, PORT))
entry_proxy.listen() 
print("\n [+] Proxy started successfully")

while True :
    print(" [-] Waiting for http request")
    client_socket,adress = entry_proxy.accept()
    print(f" [+] Connexion with {adress} established")
    request = client_socket.recv(BUFFER)
    #Chiffrement de la requête avec RSA
    request = rsa.encrypt(request, public_key)
    
    entry_proxy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    entry_proxy_client.connect((Exit_HOST, Exit_PORT))
    print(" [+] Entry_proxy successfully linked with Exit_proxy")
    entry_proxy_client.sendall(request)
    
    #Getting responses from server
    #Responses are chunked because they are cypted in RSI(4096)
    response = []
    while True :
        encrypted_data = entry_proxy_client.recv(BUFFER)
        print(f'chunk reçu : {encrypted_data}')
        try:
            response.append(encrypted_data)  #Attente réponse serveur
        except : break
        if not encrypted_data:
            break
        
    fresponse = b''
    for i in response :
        try :
            fresponse += rsa.decrypt(i, private_key)
        except: break
    print(fresponse)
    #Déchiffrage de la réponse 
    #response = rsa.decrypt(response, private_key)
    
    
    #Communication de la réponse au client
    client_socket.sendall(fresponse)
    # except : 
    #     print(" [!] The exit_proxy is not started or invalid host/port")