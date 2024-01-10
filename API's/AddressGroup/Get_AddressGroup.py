import requests
import json
import urllib3
import ssl
from time import sleep
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


### Configuração Cofre ###
ipCofre       = '192.168.10.10'
urlCofre      = f'https://{ipCofre}/BeyondTrust/api/public/v3'
workgroupName = "BeyondTrust Workgroup"
##########################


### Configuração API ###
chaveApi = 'xxxxx'
user     = 'user'
headers  = {'Authorization': f'PS-Auth key={chaveApi};' f'runas={user};'}

datype  = {'Content-type': 'application/json'}
proxy   = {'http': None,'https': None}
########################


################# Persistencia de Login #################
session             = requests.session()
session.proxies     = proxy
session.trust_env   = False
session.verify      = False
session.headers.update(headers)
#########################################################


################# LogIn #################################
def PostLogIn():
    
    login = session.post(url = f'{urlCofre}/Auth/SignAppin', verify = False) 
    
    infoLogin = login.json()
    
    userId      = infoLogin['UserId']
    userName    = infoLogin['UserName']
    name        = infoLogin['Name']
    
    print("\nLogin Feito com Sucesso! - Codigo =", login.status_code)
    print("\nUserId..:", userId, 
          "\nUserName:", userName, 
          "\nName....:", name)
    print()
#########################################################


################# Puxar informações dos Assets de um Address Group ##############################
def Get_AddressGroup():
    
    adressGroup = session.get(url = f'{urlCofre}/Addressgroups', verify = False) 
    
    infoGroup = adressGroup.json()
    adressGroup.raise_for_status()
    
    print(f"Address Group! - Codigo = {adressGroup.status_code}\n")
    
    for row in adressGroup.json():
        try:
            addressID   = row['AddressGroupID']
            addressName = row['Name']
            
            print(f"AddressGroupID - {addressID} | AddressGroupName - {addressName}")
            
        except: 
            print(f"Erro: {infoGroup}")
        
        
    addressGroupId = input("\nDigite o ID do Address Group: ")
    print()
        
    urlAdress   = f'{urlCofre}/Addressgroups/{addressGroupId}/addresses'
    address     = session.get(url = urlAdress, verify = False)
    
    infoAddress = address.json()
    address.raise_for_status()
        
    for row in address.json():
        try:
            nome_adress = row['Value']
            
            with open ("Caminhho do arquivo csv", "a") as file:
                file.write("\n" + nome_adress)
                
                print(f"[+] {nome_adress} retirado com sucesso. | Status Code = {address.status_code}")
                
        except: 
            print(f"[-] {nome_adress} não retirado. Erro: {infoAddress} | Status Code = {address.status_code}")
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify = False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Get_AddressGroup()
    PostLogOff()
    
main()
