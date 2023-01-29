# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:06:40 2023

@author: Alexandre

"""

import requests
import time

proxy = {"http": "http://localhost:9998"}

url = ["http://www.example.com",
            "http://iamjmm.ovh/",
            "http://www2.agroparistech.fr/",
            "http://forum-rallye.com/",
            "http://forum.2cv-legende.com/"]


def time_delta(url):
    t1 = time.time()
    response = requests.get("http://www.example.com", proxies=proxy)
    t2 = time.time()
    delai_proxy = t2-t1
    
    t1 = time.time()
    response = requests.get("http://www.example.com")
    t2 = time.time()
    delai_normal = t2-t1
    
    return delai_proxy-delai_normal

#Attente de 10secondes environ pour le traitement de tous les url
delais = []
for i in url:
    delais.append(time_delta(i))

print(delais)
print(f'En moyenne, en utilisant le proxy les pages mettent {sum(delais)/len(delais)} secondes supplémentaires pour charger')