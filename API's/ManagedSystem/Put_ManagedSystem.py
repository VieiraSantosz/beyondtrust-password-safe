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


################# Atualiazr informações de Managed System ##############################
def Put_ManagedSystem():
    
    systemID = 'id_do_managed_system'
    
    system_json = {
        'HostName'      : 'string',
        'IPAddress'     : 'string',
        'DnsName'       : 'string',
        'PlatformID'    : int
    }
    
    urlManagedSystem    = urlCofre + f'/ManagedSystems/{systemID}'
    managedSystem       = session.put(url = urlManagedSystem, data = system_json, verify = False) 
    
    infoSystem = managedSystem.json()
    managedSystem.raise_for_status()
    
    print(f"Managed System! - Codigo = {managedSystem.status_code}\n")
    
    try:
        ManagedSystemID = infoSystem['ManagedSystemID']
        HostName        = infoSystem['HostName']
        PlatformID      = infoSystem['PlatformID']
        
        print(f"[+] Sucesso: ManagedSystemID: {ManagedSystemID} | HostName: {HostName} |  PlatformID: {PlatformID}")
            
    except: 
        print(f"[-] Erro: {infoSystem} | Status Code = {managedSystem.status_code}")
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify = False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Put_ManagedSystem()
    PostLogOff()
    
main()
