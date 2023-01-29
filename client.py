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

proxy = {"http": "http://localhost:9998",
         "https": "http://localhost:9999"}


response = requests.get("http://www.example.com", proxies=proxy)
print(response.content)

# disable_warnings(InsecureRequestWarning)
# response2 = requests.get("https://www.code-animal.com/", proxies=proxy, verify=False)
# print(response2.content)

#http://localhost:8989/http://www.example.com
