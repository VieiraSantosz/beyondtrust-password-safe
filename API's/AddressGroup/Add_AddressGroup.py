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


################# Adicionar Máquinas no Address Group #################################
def Add_AddressGroup():
    
    adressGroup = session.get(url = f'{urlCofre}/Addressgroups', verify = False) 
   
    infoAddress = adressGroup.json()
    adressGroup.raise_for_status()
                
    print(f"Address Group - Codigo = {adressGroup.status_code}\n")
    
    for row in adressGroup.json():
        try:
            addressID   = row['AddressGroupID']
            addressName = row['Name']
            
            print(f"AddressGroupID - {addressID} | AddressGroupName - {addressName}")
            
        except: 
            print(f"Erro: {infoAddress}")
            
            
    addressGroupId = input("\nDigite o ID do Address Group: ")
    print()
    
    with open(r'Caminhho do arquivo csv') as csvfile:
    
        reader = csv.DictReader(csvfile)
    
        for row in reader:
            try:
                address_json = { 
                    'Type' : row['Type'],
                    'Value' : row['Value'], 
                    'Omit'  : row['Omit'] 
                }
    
                addressBody = json.dumps(address_json) 
        
                urlAdress   = f'{urlCofre}/AddressGroups/{addressGroupId}/Addresses'
                address     = session.post(url = urlAdress, data = addressBody, headers = datype)
                
                infoAddress = address.json()
                address.raise_for_status()
                
                print(f"[+] {row['Value']} adicionado com sucesso. | Status Code = {address.status_code}")

            except:
                print(f"[-] {row['Value']} não adicionado. Erro: {infoAddress} | Status Code = {address.status_code}")
#####################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify = False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Add_AddressGroup()
    PostLogOff()
    
main()
