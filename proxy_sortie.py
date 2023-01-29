# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 18:19:56 2023

@author: Alexandre
"""
import socket,rsa
from generate_keys import read_RSA_keys

public_key,private_key = read_RSA_keys()

HOST = 'localhost'
PORT = 9999
BUFFER = 4096

exit_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
exit_proxy.bind((HOST, PORT))
exit_proxy.listen() 
print("\n [+] Exit proxy started successfully")

while True :
    print(" [-] Waiting for the encrypted request")
    entry_proxy,adress = exit_proxy.accept()
    print(f" [+] Connexion with {adress} established")
    request = entry_proxy.recv(BUFFER)
    
    #Déchiffrage de la requête :
    request = rsa.decrypt(request, private_key)
    print(f" [+] Decrypted request : {request} ")
    target_HOST = request.decode('UTF-8').split("\n")[1].split(" ")[1].strip()
    
    exit_proxy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    exit_proxy_client.connect((target_HOST, 80))
    exit_proxy_client.sendall(request)
    response = exit_proxy_client.recv(4096)
    
    chunk_size = 256 #Because RSA 2048 can only encrypt 256bytes of data
    chunks = [response[i:i+chunk_size] for i in range(0, len(response), chunk_size)]
    
    #On chiffre la réponse
    for chunk in chunks:
        encrypted_chunk = rsa.encrypt(chunk, public_key)
        entry_proxy.send(encrypted_chunk)
        
    print(' [+] Crypted chunks successfully sent')
    entry_proxy.close()
    print(f" [-] Connexion with {adress} closed")