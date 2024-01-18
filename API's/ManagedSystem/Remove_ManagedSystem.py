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


################# Remover Managed System pelo Id #################################
def Remove_ManagedSystem_by_ID():
    
    with open(r'Caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            managedsystem_id = row['ManagedSystemID']
            
            url_get_managedsystem   = url_cofre + f"/ManagedSystems/{managedsystem_id}"
            get_managedsystem       = session.get(url = url_get_managedsystem, verify = False)
            
            info_system = get_managedsystem.json()
            
            try:
                hostname = info_system['HostName']
                
            except:
                print(f"[-] Erro: {info_system} | Status Code = {get_managedsystem.status_code}")
                break
            
            url_remove_managedsystem    = url_cofre + f"/ManagedSystems/{managedsystem_id}"
            remove_managedsystem        = session.delete(url = url_remove_managedsystem, verify=False)
            
            if (remove_managedsystem.status_code < 399):
                print(f"[+] {hostname} removido de Managed System com sucesso. | Status Code = {remove_managedsystem.status_code}")
            
            else:
                print(f"[-] {hostname} não removido de Managed System. Erro: {remove_managedsystem.json()} | Status Code = {remove_managedsystem.status_code}")
###########################################################################


################# LogOff #################################
def PostLogOff():
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Remove_ManagedSystem_by_ID()
    PostLogOff()
    
if __name__ == '__main__':
    main()
