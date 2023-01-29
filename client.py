# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:06:40 2023

@author: Alexandre

import socket

HOST = 'localhost' 
PORT = 8989

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

client.send("www.wikipedia.org".encode('UTF-8'))
"""

import requests

proxy = {"http": "http://localhost:8989", "https": "http://localhost:8989"}

#response = requests.get("http://www.example.com", proxies=proxy)
response = requests.get("https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal", proxies=proxy)
print(response.content)


#http://localhost:8989/http://www.example.com