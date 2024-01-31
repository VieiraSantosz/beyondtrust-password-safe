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
ip_cofre       = 'ip do cofre'
url_cofre      = f'https://{ip_cofre}/BeyondTrust/api/public/v3'
workgroupName  = "BeyondTrust Workgroup"
##########################


### Configuração API ###
chave_api = 'xxxxx'
user      = 'user'
headers   = {'Authorization': f'PS-Auth key={chave_api};' f'runas={user};'}

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
    
    login = session.post(url = f'{url_cofre}/Auth/SignAppin', verify = False) 
    
    info_login = login.json()
    
    userid      = info_login['UserId']
    username    = info_login['UserName']
    name        = info_login['Name']
    
    print("\nLogin Feito com Sucesso! - Codigo =", login.status_code)
    print("\nUserId..:", userid, 
          "\nUserName:", username, 
          "\nName....:", name)
    print()
#########################################################


################# Remover Managed Account pelo Id do Managed System #################################
def Remove_ManagedAccount_by_ManagedSystemID():
    
    with open(r'Caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            managedaystem_id = row['ManagedSystemID']

            url_managedsystem   = url_cofre + f'/ManagedSystems/{managedaystem_id}'
            get_managedsystem   = session.get(url = url_managedsystem, verify = False) 

            info_system = get_managedsystem.json()
            
            try:
                hostname = info_system['HostName']
                
            except:
                print(f'[-] Erro: {info_system} | Status Code = {get_managedsystem.status_code}')
                break

            url_managedaccount      = url_cofre + f"/ManagedSystems/{managedaystem_id}/ManagedAccounts"
            remove_managedaccount   = session.delete(url = url_managedaccount, verify = False)
            
            try:
                print(f"[+] Managed Account removido do '{hostname}' com sucesso. | Codigo = {remove_managedaccount.status_code}")
            
            except:
                print(f"Erro: {remove_managedaccount.json()}")  
###########################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################

def main():
    PostLogIn()
    Remove_ManagedAccount_by_ManagedSystemID()
    PostLogOff()
    
if __name__ == '__main__':
    main()
