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
    
    login = session.post(url = f'{urlCofre}/Auth/SignAppin', verify=False) 
    
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


################# Remover Managed System #################################
def Remove_ManagedSystem_by_ID():
    with open(r'C:\Users\wsantos\Documents\APIs - Netconn\ManagedSystem\.ManagedSystem.csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            Manages_SystemID = row['ManagedSystemID']
            
            urlGet          = urlCofre + f"/ManagedSystems/{Manages_SystemID}"
            managedSystem   = session.get(url = urlGet, verify = False)
            
            infoSystem = managedSystem.json()
            managedSystem.raise_for_status()
            
            HostName = infoSystem['HostName']
            
            urlRemove               = urlCofre + f"/ManagedSystems/{Manages_SystemID}"
            remove_managedsystem    = session.delete(url = urlRemove, verify=False)
            
            if (remove_managedsystem.status_code < 399):
                print(f"[+] {HostName} removido de Managed System com sucesso. | Status Code = {remove_managedsystem.status_code}")
            
            else:
                print(f"[-] {HostName} não removido de Managed System. Erro: {remove_managedsystem.json()} | Status Code = {remove_managedsystem.status_code}")
###########################################################################


################# LogOff #################################
def PostLogOff():
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Remove_ManagedSystem_by_ID()
    PostLogOff()
    
main()
