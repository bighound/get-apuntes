#!/usr/bin/python3
#
# Written by Bighound
# Description: Descarga todos tus apuntes del curso con un comando
# https://github.com/bighound/get-apuntes

import requests
import re
import string
import argparse
import os
import sys
from bs4 import BeautifulSoup

def download(asignaturas, user, pwd):
    for a in asignaturas:
        os.system('wget -r https://aulavirtual.um.es/dav/{0} --user={1} --password={2} 2>/dev/null'.format(a, user, pwd))

def login(user, pwd):
    s       = requests.Session()
    url     = "https://entrada.um.es/cas/login?service=https%3A%2F%2Faulavirtual.um.es%2Fsakai-login-tool%2Fcontainer"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username':user, 'password':pwd, '_eventId':'submit'}
    
    req   = s.post(url, headers=headers, data=payload)
    soup  = BeautifulSoup(req.text,'html.parser')
    value = soup.find('input', {'name': 'execution'}).get('value')

    payload = {'username':user, 'password':pwd, 'execution':value, '_eventId':'submit','geolocation':''}
    req  = s.post(url, data=payload)
    page = req.text
    soup = BeautifulSoup(page,'html.parser')

    asignaturas=[]
    for asign in soup.find_all('a', {'href': re.compile(".*_N_N")}):
        enlace = asign.get('href').split('/')
        asignaturas.append(enlace[len(enlace) - 1])
    
    download(asignaturas, user, pwd)

def main():
    parser = argparse.ArgumentParser(description='Descarga todos tus apuntes del curso con un sólo click.')
    parser.add_argument('--user', '-u', dest='user', help='username help')
    parser.add_argument('--pass', '-p', dest='pwd', help='password help')
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
   
    args = parser.parse_args()

    if (args.user and args.pwd is None) or (args.pwd and args.user is None):
        print("[!] Debes de introducir tanto el usuario como tu contraseña")
        sys.exit(1)

    user = args.user
    pwd  = args.pwd

    login(user, pwd)

if __name__ == '__main__':
    main()
