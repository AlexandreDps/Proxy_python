# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 18:20:56 2023

@author: Alexandre
"""
import rsa
def generate_RSA_keys(bits):
    public_key,private_key = rsa.newkeys(bits)
    with open("public.pem", "wb") as f:
        f.write(public_key.save_pkcs1("PEM"))
    with open("private.pem", "wb") as f:
        f.write(private_key.save_pkcs1("PEM"))
    print(" [+] RSA keys generated successfully")
    
def read_RSA_keys():
    with open("public.pem", "rb") as f :
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    with open("private.pem", "rb") as f :
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    print(" [+] RSA keys readed successfully")
    return public_key,private_key