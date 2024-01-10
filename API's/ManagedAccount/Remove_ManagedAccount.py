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


################# Remover Managed Account #################################
def Remove_ManagedAccount_by_ManagedSystemID():
    
    with open(r'Caminhho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            ManagedSystemID = row['ManagedSystemID']

            urlManagedSystem    = urlCofre + f'/ManagedSystems/{ManagedSystemID}'
            managedSystem       = session.get(url = urlManagedSystem, verify = False) 

            infoSystem = managedSystem.json()
            managedSystem.raise_for_status()
            
            HostName = infoSystem['HostName']

            urlRemove               = urlCofre + f"/ManagedSystems/{ManagedSystemID}/ManagedAccounts"
            remove_managedaccount   = session.delete(url = urlRemove, verify = False)
            
            remove_managedaccount.raise_for_status()
            
            if (remove_managedaccount.status_code < 399):
                print(f"Managed Account removido do '{HostName}' com sucesso. | Codigo = {remove_managedaccount.status_code}")
            
            else:
                print(f"Erro: {remove_managedaccount.json()}")  
###########################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################

def main():
    PostLogIn()
    Remove_ManagedAccount_by_ManagedSystemID()
    PostLogOff()
    
main()
