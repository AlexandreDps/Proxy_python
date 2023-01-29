# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 23:54:44 2023

@author: Alexandre
"""

import socket

HOST = 'localhost' #Pour tester on peut héberger en localhost
PORT = 8989


#On utilisera des serveurs TCP pour toutes nos opérations
#Cela semble le plus approprié pour éviter la perte de paquets
entry_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
entry_proxy.bind((HOST, PORT))

#Dans notre cas et pour les test, pas obligé de spécifier le maximum de connexions en attente 
entry_proxy.listen() 
print("Serveur proxy démarré")
while True :
    #Récupérer le socket client et son adresse lorsqu'il se connecte
    client_socket,adress = entry_proxy.accept() 
    print(f"Connexion avec {adress} établie {client_socket}")
    #Recevoir la requête du client
    request = client_socket.recv(4096)
    print("req" + str(request))
    #Extraire l'hôte de la requete GET envoyée par le client
    #exit_HOST = request.decode('UTF-8').split("\n")[1].split(" ")[1]
    
    #print("hote" + exit_HOST)
    #Proxy de sortie qui effectue la requête à notre place
    exit_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    exit_proxy.connect(('fr.wikipedia.org/wiki/Wikipédia:Accueil_principal', 80))
    exit_proxy.sendall(request)
    # Lire les données du serveur distant
    response = exit_proxy.recv(4096)

    # Transmettre les données au client
    client_socket.sendall(response)
    
    #url = client_socket.recv(1024).decode('UTF-8')
    client_socket.close()
    print(f"Connexion avec {adress} fermée")
    
    # entry_proxy.close()
    # exit_proxy.close()