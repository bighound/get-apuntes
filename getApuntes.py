#!/usr/bin/python3
#
# Written by Bighound
# Description: Descarga todos tus apuntes del curso con un comando
# https://github.com/bighound/get-apuntes

import requests
import re
import string
import argparse
import threading
import subprocess
import sys
from bs4 import BeautifulSoup

def concurrentDownload(i, subjects, user, pwd):
    subprocess.run(["wget", "-r", "https://aulavirtual.um.es/dav/{0}".format(subjects[i]), "--user={0}".format(user),"--password={0}".format(pwd),"2>&2"])

def login(user, pwd):
    s       = requests.Session()
    url     = "https://entrada.um.es/cas/login?service=https%3A%2F%2Faulavirtual.um.es%2Fsakai-login-tool%2Fcontainer"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username':user, 'password':pwd, '_eventId':'submit'}
    
    req   = s.post(url, headers=headers, data=payload)
    if req.status_code != 200:
        print("[!] El login es incorrecto, prueba con otras credenciales.")
        sys.exit(1)

    soup  = BeautifulSoup(req.text,'html.parser')
    value = soup.find('input', {'name': 'execution'}).get('value')
    if (value is None):
        print("[!] No se ha podido obtener la información necesaria.")
        sys.exit(1)

    payload = {'username':user, 'password':pwd, 'execution':value, '_eventId':'submit','geolocation':''}
    req  = s.post(url, data=payload)
    if req.status_code != 200:
        print("[!] El login es incorrecto, prueba con otras credenciales.")
        sys.exit(1)

    page = req.text
    soup = BeautifulSoup(page,'html.parser')

    subjects=[]
    for subj in soup.find_all('a', {'href': re.compile(".*_N_N")}):
        link = subj.get('href').split('/')
        subjects.append(link[len(link) - 1])
    
    threads = list()
    for i in range(len(subjects)):
        t = threading.Thread(target=concurrentDownload, args=(i, subjects, user, pwd))
        threads.append(t)
        t.start()

def main():
    parser = argparse.ArgumentParser(description='Descarga todos tus apuntes del curso con un sólo click.')
    parser.add_argument('--user', '-u', dest='user', help='username help')
    parser.add_argument('--pass', '-p', dest='pwd', help='password help')
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
   
    args = parser.parse_args()

    if (args.user is None or args.pwd is None):
        print("[!] Debes de introducir tanto el usuario como tu contraseña")
        sys.exit(1)

    if (args.user == "" or args.pwd == ""):
        print("[!] El usuario o la contraseña no pueden estar vacíos.")
        sys.exit(1)

    user = args.user
    pwd  = args.pwd

    emailFormat = re.search("[a-zA-Z]+[0-9]*@um.es", user)
    if (emailFormat is None):
        print("[!] El correo es incorrecto. Ej: example@um.es")
        sys.exit(1)

    login(user, pwd)

if __name__ == '__main__':
    main()
